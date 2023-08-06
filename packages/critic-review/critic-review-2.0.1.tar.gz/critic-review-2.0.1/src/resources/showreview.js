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

function archiveBranch()
{
  function finished(result)
  {
    if (result)
    {
      var done = $("<div class=operation-performed title=Status>" +
                   "<h1>Branch archived</h1>" +
                   "</div>");

      done.dialog({
        modal: true,
        buttons: {
          OK: function () {
            done.dialog("close");
            location.reload();
          }
        }
      });
    }
  }

  var operation = new Operation({
    action: "archive branch",
    url: "archivebranch",
    data: { review_id: review.id },
    callback: finished
  });

  operation.execute();
}

function resurrectBranch()
{
  function finish(result)
  {
    if (result)
    {
      var scheduled_archival_note = "";

      if (result.delay)
      {
        var delay = String(result.delay) + " day";
        if (result.delay > 1)
          delay += "s";
        scheduled_archival_note = (
          "<p>Note that since the review is not open, its branch was " +
          "scheduled to be archived again in " + delay + ".</p>");
      }

      var done = $("<div class=operation-performed title=Status>" +
                   "<h1>Branch resurrected</h1>" +
                   scheduled_archival_note +
                   "</div>");

      done.dialog({
        width: scheduled_archival_note ? 600 : void 0,
        modal: true,
        buttons: {
          OK: function () {
            done.dialog("close");
            location.reload();
          }
        }
      });
    }
  }

  var operation = new Operation({
    action: "resurrect branch",
    url: "resurrectbranch",
    data: { review_id: review.id },
    callback: finish
  });

  operation.execute();
}

function shortDate(date)
{
  function pad(number, width)
  {
    var result = String(number);
    while (result.length < width)
      result = "0" + result;
    return result;
  }

  return (pad(date.getFullYear(), 4) +
          "-" + pad(date.getMonth() + 1, 2) +
          "-" + pad(date.getDate(), 2) +
          " " + pad(date.getHours(), 2) +
          ":" + pad(date.getMinutes(), 2));
}

function triggerUpdate(branch_id)
{
  var operation = new Operation({ action: "trigger update",
                                  url: "triggertrackedbranchupdate",
                                  data: { branch_id: branch_id }});

  if (operation.execute())
  {
    var done = $("<div title='Status' style='text-align: center; padding-top: 2em'>Branch update triggered.</div>");
    done.dialog({ modal: true, buttons: { OK: function () { done.dialog("close"); }}});
  }
}

function enableTracking(branch_id, remote, current_remote_name)
{
  function finish()
  {
    var operation = new Operation({ action: "enable tracking",
                                    url: "enabletrackedbranch",
                                    data: { branch_id: branch_id,
                                            new_remote_name: remote_name.val() }});

    return Boolean(operation.execute());
  }

  var self = this;
  var content = $("<div class='enabletracking' title='Enable Tracking'><p><b>Remote branch name:</b><br><input></p></div>");
  var remote_name = content.find("input");

  remote_name
    .val(current_remote_name)
    .autocomplete({ source: AutoCompleteRef(remote, "refs/heads/"), html: true });

  var buttons = {
    "Enable Tracking": function () { if (finish()) { content.dialog("close"); location.reload(); } },
    "Cancel": function () { content.dialog("close"); }
  };

  content.dialog({ width: 400,
                   buttons: buttons });
}

function disableTracking(branch_id)
{
  var operation = new Operation({ action: "disable tracking",
                                  url: "disabletrackedbranch",
                                  data: { branch_id: branch_id }});

  if (operation.execute())
    location.reload();
}

function watchReview()
{
  var operation = new Operation({ "action": "watch review",
                                  "url": "watchreview",
                                  "data": { "review_id": review.id,
                                            "subject_name": user.name }});

  if (operation.execute())
    location.reload();
}

function unwatchReview()
{
  var operation = new Operation({ "action": "unwatch review",
                                  "url": "unwatchreview",
                                  "data": { "review_id": review.id,
                                            "subject_name": user.name }});

  if (operation.execute())
    location.reload();
}

function filterPartialChanges()
{
  var content = $("<div title='Filter Partial Changes'>Please select the desired range of commits below using click-and-drag.</div>");

  function cancel()
  {
    content.dialog("close");
    overrideShowSquashedDiff = null;
  }

  content.dialog({ width: 800,
                   position: "top",
                   buttons: { Cancel: cancel },
                   resizable: false });

  overrideShowSquashedDiff = function (from_sha1, to_sha1)
    {
      overrideShowSquashedDiff = null;
      content.dialog("close");

      location.href = "/filterchanges?review=" + review.id + "&first=" + from_sha1 + "&last=" + to_sha1;
    };
}

function updateFilters(filter_type)
{
  function addFilters(names, path)
  {
    var operation = new Operation({
      action: "add review filters",
      url: "addreviewfilters",
      data: { review_id: review.id,
              filters: [{ type: filter_type,
                          user_names: names,
                          paths: [path] }] }
    });

    return operation.execute() != null;
  }

  addReviewFiltersDialog({
    filter_type: filter_type,
    callback: addFilters,
    reload_page: true
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

function removeReviewFilter(filter_id, filter_user, filter_type, filter_path, confirm)
{
  function finish()
  {
    var operation = new Operation({ action: "remove review filter",
                                    url: "removereviewfilter",
                                    data: { filter_id: filter_id }});

    if (operation.execute())
    {
      location.reload();
      return true;
    }
    else
      return false;
  }

  if (confirm)
  {
    var content = $("<div class='removefilter' title='Confirm'><p>Please confirm that you mean to remove the filter that makes</p><div class=user>" + htmlify(filter_user) + "</div><p>a " + filter_type + " of</p><div class=path>" + filter_path + "</div><p>An email will be sent the user about the change and its effect on assignments.</p></div>");

    content.dialog({ width: 400,
                     buttons: { "Remove the filter": function () { if (finish()) content.dialog("close"); },
                                "Do nothing": function () { content.dialog("close"); } },
                     modal: true });
  }
  else
    finish();
}

function applyFilters(what)
{
  var query_url, apply_url;

  if (what == "global")
  {
    query_url = "queryglobalfilters";
    apply_url = "applyglobalfilters";
  }
  else
  {
    query_url = "queryparentfilters";
    apply_url = "applyparentfilters";
  }

  function openDialog(result)
  {
    if (!result)
      return;

    function proceed()
    {
      function finish(result)
      {
        if (result)
        {
          dialog.dialog("close");
          location.reload();
        }
      }

      var operation = new Operation({ action: "update review filters",
                                      url: apply_url,
                                      data: { review_id: review.id },
                                      wait: "Applying filters ...",
                                      callback: finish });

      operation.execute();
    }

    function cancel()
    {
      dialog.dialog("close");
    }

    var html = "<div title='Apply " + what + " filters'>";
    var buttons = {};

    if (result.reviewers.length || result.watchers.length)
    {
      html += ("<p>By applying " + what + " filters to this review, the " +
               "following new reviewers and watchers would be added:</p>");

      if (result.reviewers.length)
      {
        html += "<p>New reviewers:</p><ul>";
        result.reviewers.forEach(
          function (user)
          {
            html += "<li>" + htmlify(user.displayName + " <" + user.email + ">") + "</li>";
          });
        html += "</ul>";
      }

      if (result.watchers.length)
      {
        html += "<p>New watchers:</p><ul>";
        result.watchers.forEach(
          function (user)
          {
            html += "<li>" + htmlify(user.displayName + " <" + user.email + ">") + "</li>";
          });
        html += "</ul>";
      }

      buttons["Apply Filters"] = proceed;
    }
    else
    {
      html += ("<p>Applying " + what + " filters to this review would " +
               "not cause any immediate changes.  It may however affect " +
               "what happens when adding additional changes to the review " +
               "in the future.</p>");
    }

    buttons["Cancel"] = cancel;

    html += "</div>";

    var dialog = $(html);

    dialog.dialog({ width: 400, modal: true, buttons: buttons });
  }

  var operation = new Operation({ action: "query review filters",
                                  url: query_url,
                                  data: { review_id: review.id },
                                  wait: "Listing new reviewers and watchers ...",
                                  callback: openDialog });

  operation.execute();
}

function toggleReviewFilters(type, button)
{
  var table = $("table.reviewfilters." + type);
  var tbody = table.find("tbody");
  var tfoot = table.find("tfoot");

  if (tbody.hasClass("hidden"))
  {
    tbody.removeClass("hidden");
    tfoot.addClass("hidden");
    button.button("option", "label", "Hide Custom Filters");
  }
  else
  {
    tbody.addClass("hidden");
    tfoot.removeClass("hidden");
    button.button("option", "label", "Show Custom Filters");
  }
}

function prepareRebase()
{
  var rebase_type_dialog;

  function finish()
  {
    var inplace = rebase_type_dialog.find("input#inplace:checked").size() != 0;

    if (inplace)
    {
      var operation = new Operation({ action: "prepare rebase",
                                      url: "preparerebase",
                                      data: { review_id: review.id }});

      if (operation.execute())
      {
        rebase_type_dialog.dialog("close");

        var finished =
          $("<div title='Rebase Prepared!'>"
          +   "<p>"
          +     "You may now push the rebased branch, using \"git push -f\".  "
          +     "Any attempt to push changes to this review by other users will "
          +     "be rejected until you've completed the rebase, or aborted it."
          +   "</p>"
          +   "<p>"
          +     "<b>Note:</b> Remember that one commit on the rebased branch must "
          +     "reference a tree that is identical to the one referenced by the "
          +     "current head of the review branch.  If this is not the case, your "
          +     "push will be rejected."
          +   "</p>"
          + "</div>");

        finished.dialog({ width: 400,
                          modal: true,
                          close: function() { location.reload(); },
                          buttons: { Close: function () { finished.dialog("close"); }}
                        });
      }
    }
    else
    {
      rebase_type_dialog.dialog("close");

      var select_upstream_dialog =
        $("<div class='specifyupstream' title='Specify New Upstream Commit'>"
        +   "<p>"
        +     "Unless you squashed the whole branch into a single commit, please specify "
        +     "the new upstream commit onto which the review branch is rebased, either by "
        +     "entering a SHA-1 sum or by selecting one of the suggested tags:"
        +   "</p>"
        +   "<p>"
        +     "<label><input name='single' type='checkbox'>Branch squashed into a single commit.</label>"
        +   "</p>"
        +   "<p>"
        +     "<b>SHA-1:</b><input name='sha1' size=40 spellcheck='false'>"
        +   "</p>"
        +   "<p>"
        +     "<b>Tag:</b>"
        +     "<select disabled>"
        +       "<option value='none'>Fetching suggestions...</option>"
        +     "</select>"
        +   "</p>"
        + "</div>");

      var select_upstream_dialog_closed = false;

      function populateSuggestedUpstreams(result)
      {
        if (result)
        {
          var upstreams = result.upstreams.map(
            function (tag)
            {
              return "<option value='" + htmlify(tag) + "'>" + htmlify(tag) + "</option>";
            });

          var select = select_upstream_dialog.find("select").get(0);

          if (upstreams.length != 0)
          {
            select.innerHTML = "<option value='none'>Found " + upstreams.length + " likely upstreams:</option>" + upstreams.join("");
            select.disabled = single.checked;
          }
          else
            select.innerHTML = "<option value='none'>(No likely upstreams found.)</option>";
        }
      }

      var fetch_upstreams = new Operation({ action: "fetch suggested upstream commits",
                                            url: "suggestupstreams",
                                            data: { review_id: review.id },
                                            callback: populateSuggestedUpstreams });

      fetch_upstreams.execute();

      var single = select_upstream_dialog.find("input").get(0);
      var sha1 = select_upstream_dialog.find("input").get(1);
      var tag = select_upstream_dialog.find("select").get(0);

      single.onclick = function ()
        {
          sha1.disabled = single.checked;
          tag.disabled = single.checked || tag.options.length == 1;
        };

      function finishMove()
      {
        var upstream;

        if (single.checked)
          upstream = "0000000000000000000000000000000000000000";
        else if (tag.value != "none" && sha1.value != "")
          alert("Ambiguous input! Please leave either SHA-1 or tag empty.");
        else if (tag.value == "none" && !/^[0-9a-f]{40}$/i.test(sha1.value))
          alert("Invalid input! Please specify a full 40-character SHA-1 sum.");
        else if (sha1.value != "")
          upstream = sha1.value;
        else
          upstream = tag.value;

        if (typeof upstream == "string")
        {
          var operation = new Operation({ action: "prepare rebase",
                                          url: "preparerebase",
                                          data: { review_id: review.id,
                                                  new_upstream: upstream }});

          if (operation.execute())
          {
            select_upstream_dialog.dialog("close");

            var finished =
              $("<div title='Rebase Prepared!'>"
              +   "<p>"
              +     "You may now push the rebased branch, using \"git push -f\".  "
              +     "Any attempt to push changes to this review by other users will "
              +     "be rejected until you've completed the rebase, or aborted it."
              +   "</p>"
              +   "<p>"
              +     "<b>Important:</b> Remember not to push any new changes to the "
              +     "review with this push; such changes will be very difficult to "
              +     "see or review."
              +   "</p>"
              + "</div>");

            finished.dialog({ width: 400,
                              modal: true,
                              close: function() { location.reload(); },
                              buttons: { Close: function () { finished.dialog("close"); }}
                            });
          }
        }
      }

      select_upstream_dialog.dialog({ width: 400,
                                      modal: true,
                                      buttons: { Continue: function () { finishMove(); },
                                                 Cancel: function () { select_upstream_dialog.dialog("close"); }},
                                      close: function () { select_upstream_dialog_closed = true; }
                                    });
    }

    return true;
  }

  function start(supports_move)
  {
    rebase_type_dialog =
      $("<div title='Prepare Rebase'>"
      +   "<p>Please select rebase type:</p>"
      +   "<dl>"
      +     "<dt><label><input id='inplace' type='radio' name='rebasetype' checked>History Rewrite / In-place</label></dt>"
      +     "<dd>Rebase on-top of the same upstream commit that only changes the history on the branch.</dd>"
      +     "<dt><label><input id='move' type='radio' name='rebasetype'" + (supports_move ? "" : " disabled") + ">New Upstream / Move</label></dt>"
      +     "<dd>" + (supports_move ? "" : "<div class='notsupported'>[Not supported for this review!]</div>") + "Rebase on-top of a different upstream commit.  Can also change the history on the branch in the process.</dd>"
      +   "</dl>"
      + "</div>");

    rebase_type_dialog.dialog({ width: 400,
                                modal: true,
                                buttons: { Continue: function () { finish(); },
                                           Cancel: function () { rebase_type_dialog.dialog("close"); }}
                              });
  }

  var operation = new Operation({ action: "check rebase possibility",
                                  url: "checkrebase",
                                  data: { review_id: review.id }});

  var result = operation.execute();

  if (result)
    start(result.available == "both");
}

function cancelRebase()
{
  var operation = new Operation({ action: "cancel rebase",
                                  url: "cancelrebase",
                                  data: { review_id: review.id }});

  if (operation.execute())
    location.reload();
}

function revertRebase(rebase_id)
{
  var confirm_dialog = $("<div title=Please Confirm'><p>Are you sure you want to revert the rebase?</p></div>");

  function finish()
  {
    var operation = new Operation({ action: "revert rebase",
                                    url: "revertrebase",
                                    data: { review_id: review.id,
                                            rebase_id: rebase_id }});

    if (operation.execute())
    {
      confirm_dialog.dialog("close");
      location.reload();
    }
  }

  confirm_dialog.dialog({ width: 400,
                          modal: true,
                          buttons: { "Revert Rebase": function () { finish(); },
                                     "Do Nothing": function () { confirm_dialog.dialog("close"); }}
                        });
}

function excludeRecipient(user_id)
{
  var operation = new Operation({ action: "exclude recipient",
                                  url: "addrecipientfilter",
                                  data: { review_id: review.id,
                                          user_id: user_id,
                                          include: false }});

  if (operation.execute())
    location.reload();
}

function includeRecipient(user_id)
{
  var operation = new Operation({ action: "include recipient",
                                  url: "addrecipientfilter",
                                  data: { review_id: review.id,
                                          user_id: user_id,
                                          include: true }});

  if (operation.execute())
    location.reload();
}

$(document).ready(function ()
  {
    $("button.archive").click(archiveBranch);
    $("button.resurrect").click(resurrectBranch);

    $("tr.commit td.summary").each(function (index, element)
      {
        var users = $(element).attr("critic-reviewers");
        if (users)
        {
          users = users.split(",");

          $(element).find("a.commit").tooltip({
            items: 'a.commit',
            content: function ()
              {
                var html = "<div class='summary-tooltip'><div class='header'>Needs review from</div>";

                for (var index = 0; index < users.length; ++index)
                {
                  var match = /([^:]+):(current|absent|retired)/.exec(users[index]);
                  var fullname = match[1];
                  var status = match[2];
                  if (status != "retired")
                  {
                    html += "<div class='reviewer'>" + htmlify(fullname);
                    if (status == "absent")
                      html += "<span class='absent'> (absent)</span>";
                    html += "</div>";
                  }
                }

                return $(html + "</div>");
              },
            track: true,
            hide: false
          });
        }
      });

    $("td.straggler.no-email").each(function (index, element)
      {
        $(element).tooltip({
          items: 'td.straggler.no-email',
          content: function ()
            {
              return $("<div class='no-email-tooltip'><strong>This user has not enabled the <u>email.activated</u> preference!</strong></div>");
            },
          track: true,
          hide: false
        });
      });

    $("a[title]").tooltip({ fade: 250 });

    var reviewfilters = [];

    $("table.shared button.accept").click(function (ev)
      {
        var target = $(ev.currentTarget);
        var paths = JSON.parse(target.attr("critic-paths"));
        var user_ids = JSON.parse(target.attr("critic-user-ids"));

        reviewfilters.push({ type: "watcher",
                             user_ids: user_ids,
                             paths: paths });

        $("table.shared td.buttons > span").css("display", "inline");

        target.parents("td.buttons").children("button").css("visibility", "hidden");
        target.parents("tr.reviewers").children("td.willreview").css("text-decoration", "line-through");
      });

    $("table.shared button.deny").click(function (ev)
      {
        var target = $(ev.currentTarget);
        var paths = JSON.parse(target.attr("critic-paths"));

        reviewfilters.push({ type: "watcher",
                             user_ids: [user.id],
                             paths: paths });

        $("table.shared td.buttons > span").css("display", "inline");

        target.parents("td.buttons").children("button").css("visibility", "hidden");
        target.parents("tr.reviewers").find("td.willreview span.also").css("text-decoration", "line-through");
      });

    $("table.shared button.cancel").click(function (ev)
      {
        location.reload();
      });

    $("table.shared button.confirm").click(function (ev)
      {
        var operation = new Operation({ action: "add review filters",
                                        url: "addreviewfilters",
                                        data: { review_id: review.id,
                                                filters: reviewfilters }});

        if (operation.execute())
        {
          $("table.shared td.buttons > span").css("display", "none");
          reviewfilters = [];
          location.reload();
        }
      });

    $("button.preparerebase").click(prepareRebase);
    $("button.cancelrebase").click(cancelRebase);
  });
