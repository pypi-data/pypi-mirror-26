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

$(function () {
  var fields = $("input.field");
  var submit = $("input.login");
  var form = $("form");

  fields.each(function (index) {
    $(this).keypress(function (ev) {
      if (ev.keyCode == 13) {
        if (index == fields.length - 1)
          submit.click();
        else
          fields[index + 1].focus();
      }
    });
  });

  submit.button();

  form.submit(function (ev) {
    var data = {
      fields: {}
    };

    fields.each(function () {
      data.fields[this.name] = this.value;
    });

    var operation = new Operation({
      action: "login",
      url: "validatelogin",
      data: data
    });

    var result = operation.execute();

    if (!result || result.message) {
      ev.preventDefault();

      if (result) {
        $("tr.status td").text(result.message);
        $("tr.status").removeClass("disabled");
      }
    }
  });
});
