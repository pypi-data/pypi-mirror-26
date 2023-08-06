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

$(function ()
  {
    $("td.repositories select").change(function (ev)
      {
        if (typeof repository == "undefined" || ev.target.value != repository.id)
          location.href = "/branches?repository=" + encodeURIComponent(ev.target.value);
      });

    $(".repository-select").chosen({
      inherit_select_classes: true,
      generate_selected_value: function (item)
        {
          return { html: "Repository: <b>" + htmlify(item.text) + "</b>" };
        },
      collapsed_width: "auto",
      expanded_width: "600px"
    });
  });
