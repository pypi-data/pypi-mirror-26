/* -*- mode: js; indent-tabs-mode: nil -*-

 Copyright 2012 Jens Lindström, Opera Software ASA

 Licensed under the Apache License, Version 2.0 (the "License"); you may not
 use this file except in compliance with the License.  You may obtain a copy of
 the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 License for the specific language governing permissions and limitations under
 the License.

*/

/* -*- Mode: js; js-indent-level: 2; indent-tabs-mode: nil -*- */

var reviewfilters = {};
var recipients_mode = "opt-out", recipients_included = {}, recipients_excluded = {};

function splitReviewFilters(reviewfilters)
{
  var result = [];
  for (var key in reviewfilters)
  {
    var data = JSON.parse(key);
    data.type = reviewfilters[key];
    result.push(data);
  }
  return result;
}

function submitReview()
{
  var branch_name = document.getElementById("branch_name");
  var summary = document.getElementById("summary");
  var description = document.getElementById("description").value.trim();

  if (invalid_branch_name && branch_name.value == invalid_branch_name)
  {
    alert("You need to edit the branch name, lazy!");
    branch_name.focus();
    return;
  }

  if (branch_name.value.length <= 4)
  {
    alert("A branch name that short is not a good review identifier.  Please elaborate a little bit.");
    branch_name.focus();
    return;
  }

  if (summary.value.length <= 8)
  {
    alert("A summary that short is not very meaningful.  Please elaborate a little bit.");
    summary.focus();
    return;
  }

  var data = { repository_id: repository.id,
               commit_ids: review_data.commit_ids,
               branch: "r/" + branch_name.value,
               summary: summary.value.trim(),
               reviewfilters: splitReviewFilters(reviewfilters),
               recipientfilters: { mode: recipients_mode,
                                   included: Object.keys(recipients_included),
                                   excluded: Object.keys(recipients_excluded) },
               applyfilters: $("input.applyfilters:checked").size() != 0,
               applyparentfilters: $("input.applyparentfilters:checked").size() != 0 };

  if (description)
    data.description = description;
  if (typeof fromBranch == "string")
    data.frombranch = fromBranch;
  if (typeof trackedbranch == "object")
    data.trackedbranch = trackedbranch;

  var operation = new Operation({ action: "create review",
                                  url: "submitreview",
                                  data: data });
  var result = operation.execute();

  if (result)
  {
    if (result.extensions_output)
      showMessage("Review Created",
                  "Extension Output",
                  "<pre>" + htmlify(result.extensions_output) + "</pre>",
                  function () { location.href = "/r/" + result.review_id; });
    else
      location.href = "/r/" + result.review_id;
  }
}

function updateReviewersAndWatchers(new_reviewfilters)
{
  var success = false;

  if (!new_reviewfilters)
    new_reviewfilters = reviewfilters;

  var data = { repository_id: repository.id,
               commit_ids: review_data.commit_ids,
               reviewfilters: splitReviewFilters(new_reviewfilters),
               applyfilters: $("input.applyfilters:checked").size() != 0,
               applyparentfilters: $("input.applyparentfilters:checked").size() != 0 };

  var operation = new Operation({ action: "update filters",
                                  url: "reviewersandwatchers",
                                  data: data });
  var result = operation.execute();

  if (result)
  {
    $("table.filters").replaceWith(result.html);
    $("table.filters").find("button").button();

    connectApplyFilters();

    reviewfilters = new_reviewfilters;
    return true;
  }
  else
    return false;
}

function updateFilters(filter_type)
{
  function addFilters(names, path)
  {
    new_reviewfilters = {};

    for (var key in reviewfilters)
      new_reviewfilters[key] = reviewfilters[key];

    names.forEach(
      function (name)
      {
        var key = JSON.stringify({ username: name, path: path });
        new_reviewfilters[key] = filter_type;
      });

    return updateReviewersAndWatchers(new_reviewfilters);
  }

  addReviewFiltersDialog({
    filter_type: filter_type,
    callback: addFilters,
    reload_page: false
  });
}

function addReviewer()
{
  updateFilters("reviewer");
}

function addWatcher()
{
  updateFilters("watcher");
}

function editRecipientList()
{
  var recipient_list_dialog =
    $("<div id='recipients' title='Edit Recipient List'>"
    +   "<p>The recipient list determines the list of users that receive "
    +      "e-mails about various updates to the review.  The recipient "
    +      "list is constructed from the list of users associated with the "
    +      "review (reviewers and watchers) either in an opt-in or opt-out "
    +      "fashion.  The default is opt-out, meaning all associated users "
    +      "receive e-mails unless they specifically ask not to.  By "
    +      "choosing opt-in mode, the review owner can restrict the list "
    +      "of recipients.</p>"
    +   "<p>Note: the review owner (you) is always included in the "
    +      "recipient list.</p>"
    +   "<table>"
    +     "<tr><td class=key>Mode:</td><td class=value>"
    +       "<select id='mode'>"
    +         "<option value='opt-out'>Opt-out (all users not specified below receive e-mails)</option>"
    +         "<option value='opt-in'>Opt-in (only users specified below receive e-mails)</option>"
    +       "</select>"
    +     "</td></tr>"
    +     "<tr><td class=key>Users:</td><td class=value>"
    +       "<input id='users'>"
    +     "</td></tr>"
    +   "</table>"
    + "</div>");

  if (recipients_mode == "opt-out")
    names = Object.keys(recipients_excluded);
  else
    names = Object.keys(recipients_included);

  recipient_list_dialog.find("#mode").val(recipients_mode);
  recipient_list_dialog.find("#users").val(names.join(", "));

  function save()
  {
    recipients_mode = recipient_list_dialog.find("#mode").val();
    recipients_included = {};
    recipients_excluded = {};

    var users = recipient_list_dialog.find("#users").val().split(/[\s,]+/g);
    for (var index = 0; index < users.length; ++index)
    {
      var name = users[index];
      if (name)
        if (recipients_mode == "opt-in")
          recipients_included[name] = true;
        else
          recipients_excluded[name] = true;
    }

    var mode;

    if (recipients_mode == "opt-in")
      if (Object.keys(recipients_included).length != 0)
      {
        mode = "No-one except ";
        users = Object.keys(recipients_included);
      }
      else
        mode = "No-one at all";
    else
      if (Object.keys(recipients_excluded).length != 0)
      {
        mode = "Everyone except ";
        users = Object.keys(recipients_excluded);
      }
      else
        mode = "Everyone";

    $("span.mode").text(mode);

    if (users)
      $("span.users").text(users.join(", "));

    recipient_list_dialog.dialog("close");
  }

  function cancel()
  {
    recipient_list_dialog.dialog("close");
  }

  function handleKeypress(ev)
  {
    if (ev.keyCode == 13)
      save();
  }

  recipient_list_dialog.find("#users").keypress(handleKeypress);

  recipient_list_dialog.dialog({ width: 620,
                                 modal: true,
                                 buttons: { Save: save, Cancel: cancel }});

  function enableAutoCompletion(result)
  {
    recipient_list_dialog.find("#users").autocomplete(
      { source: AutoCompleteUsers(result.users) });
  }

  var operation = new Operation({ action: "get auto-complete data",
                                  url: "getautocompletedata",
                                  data: { values: ["users"] },
                                  callback: enableAutoCompletion });

  operation.execute();
}

function connectApplyFilters()
{
  $("tr.applyfilters").click(function (ev)
    {
      if (ev.target.nodeName.toLowerCase() != "input")
      {
        var checkbox = $(ev.currentTarget).find("input");
        checkbox.get(0).checked = !checkbox.get(0).checked;
        updateReviewersAndWatchers();
      }
    });

  $("tr.applyfilters input").click(function (ev)
    {
      updateReviewersAndWatchers();
    });
}

$(document).ready(function ()
  {
    connectApplyFilters();

    $(".repository-select")
      .change(
        function ()
        {
          var name = $(this).val();

          if (default_remotes[name])
            $("input.remote").val(default_remotes[name]);

          if (default_branches[name])
            $("input.upstreamcommit").val(default_branches[name] ? "refs/heads/" + default_branches[name] : "");
        })
      .chosen({ inherit_select_classes: true });

    function getCurrentRemote()
    {
      var remote = $("input.remote").val();
      if (!remote)
        return undefined;
      return remote.trim();
    }

    var input_workbranch = $("input.workbranch");

    input_workbranch.autocomplete({ source: AutoCompleteRef(getCurrentRemote, "refs/heads/"), html: true });
    input_workbranch.keypress(
      function (ev)
      {
        if (ev.keyCode == 13)
          $("button.fetchbranch").click();
      });

    var input_upstreamcommit = $("input.upstreamcommit");

    input_upstreamcommit.autocomplete({ source: AutoCompleteRef(), html: true });

    $("button.fetchbranch").click(
      function ()
      {
        var branch = $("input.workbranch").val().trim();
        var upstream = $("input.upstreamcommit").val().trim();

        if (!branch)
        {
          showMessage("Invalid input!", "Invalid input!", "Please provide a non-empty branch name.");
          return;
        }

        if (!upstream)
        {
          showMessage("Invalid input!", "Invalid input!", "Please provide a non-empty upstream commit reference.");
          return;
        }

        function finish(result)
        {
          if (result)
            location.href = ("/createreview" +
                             "?repository=" + encodeURIComponent($("select.repository-select").val().trim()) +
                             "&commits=" + encodeURIComponent(result.commit_ids) +
                             "&remote=" + encodeURIComponent(getCurrentRemote()) +
                             "&branch=" + encodeURIComponent(branch) +
                             "&upstream=" + encodeURIComponent(upstream) +
                             "&reviewbranchname=" + encodeURIComponent(branch));
        }

        var operation = new Operation({ action: "fetch remote branch",
                                        url: "fetchremotebranch",
                                        data: { repository_name: $("select.repository-select").val().trim(),
                                                remote: getCurrentRemote(),
                                                branch: branch,
                                                upstream: upstream },
                                        wait: "Fetching branch...",
                                        callback: finish });

        operation.execute();
      });

    if (getCurrentRemote())
      input_workbranch.focus();
    else
      $("input.remote").focus();
  });
