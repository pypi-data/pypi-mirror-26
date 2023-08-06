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

"use strict";

$(function () {
  var searchForm = document.forms.search;

  function doSearch(query) {
    function handleResult(table, result) {
      $(".search-result")
        .css({ display: "block" })
        .children(".callout").empty().append(table);
      history.replaceState(null, null, "/search?" + result.query_string);
    }

    quickSearch(query, searchForm.query ? handleResult : null);
  }

  if (!searchForm.query) {
    // Disable the freetext input if none of its checkboxes are checked
    [ searchForm.freetextSummary, searchForm.freetextDescription ].forEach(
      function (checkbox, idx, checkboxes) {
        checkbox.addEventListener('click', function () {
          var someChecked = checkboxes.some(
            function (cbox) { return cbox.checked; }
          );
          if (searchForm.freetext.disabled === someChecked) {
            searchForm.freetext.disabled = !someChecked;
          }
        });
      });
  }

  searchForm.addEventListener('submit', function (evt) {
    evt.preventDefault();
    var form = this;
    function phrases(value)
    {
      return value.match(/"[^"]+"|'[^']+'|\S+/g).map(
        function (phrase)
        {
          var match = /^'([^']+)'|"([^"]+)"$/.exec(phrase);
          if (match)
            return match[1] || match[2] || "";
          else
            return phrase;
        });
    }

    function tokens(value)
    {
      return value.split(/[\s,]+/g).map(
        function (item)
        {
          return item.trim();
        }).filter(
          Boolean
        );
    }

    function with_keyword(keyword)
    {
      return function (term) { return term ? keyword + ":'" + term + "'" : ""; };
    }

    var query;

    if (form.query) {
      query = form.query.value.trim();
    } else {
      var terms = [];

      var freetext = form.freetext.value.trim();
      if (freetext) {
        var textphrases = phrases(freetext);
        if (form.freetextSummary.checked && form.freetextDescription.checked) {
          terms.push.apply(terms, textphrases.map(with_keyword("text")));
        } else if (form.freetextSummary.checked) {
          terms.push.apply(terms, textphrases.map(with_keyword("summary")));
        } else if (form.freetextDescription.checked) {
          terms.push.apply(terms, textphrases.map(with_keyword("description")));
        }
      }

      var users = tokens(form.user.value.trim()), usersKey;
      if (form.userOwner.checked && form.userReviewer.checked) {
        usersKey = "owner-or-reviewer";
      } else if (form.userOwner.checked) {
        usersKey = "owner";
      } else if (form.userReviewer.checked) {
        usersKey = "reviewer";
      } else {
        usersKey = "user";
      }
      terms.push.apply(terms, users.map(with_keyword(usersKey)));

      var repository = form.repository.value;
      if (repository) {
        terms.push(with_keyword("repository")(repository));
      }

      var branch = form.branch.value.trim();
      if (branch) {
        terms.push(with_keyword("branch")(branch));
      }

      var paths = tokens(form.path.value.trim());
      terms.push.apply(terms, paths.map(with_keyword("path")));

      var state = form.state.value;
      if (state) {
        terms.push(with_keyword("state")(state));
      }

      query = terms.join(" ");
    }

    doSearch(query);
  });

  $(document.forms.search.user)
    .autocomplete({ source: AutoCompleteUsers(users) });

  $("select[name='state']").chosen();

  $(".repository-select")
    .chosen({ inherit_select_classes: true,
              allow_single_deselect: true,
              collapsed_width: "100%",
              expanded_width: "40em" });

  if (searchForm.query && searchForm.query.value.trim()) {
    doSearch(searchForm.query.value.trim());
  }
});
