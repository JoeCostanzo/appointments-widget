var addBtn;
var newBtn;
var appointmentForm;

function getData(url, callback, params) {
  if (params) {
    return $.getJSON(url, params)
      .done(function(json) {
        callback(json);
      })
      .error(function(d,e) { alert(e)});
  }
  $.getJSON(url, callback)
    .error(function(d,e) { alert(e)});
}

function formatResponse_PopulateTable(response) {
  $('#appointments_table').empty();
  var trHTML = '<thead><tr><th>Date</th><th>Time</th><th>Description</th></tr></thead><tbody>';
  if (response) {
    $.each(response, function (i, item) {
      trHTML += '<tr><td>' + item.Date + '</td><td>'
        + item.Time + '</td><td>' + item.Description + '</td></tr>';
    });
  }
  $('#appointments_table').append(trHTML += '</tbody>');
}

function getAppointments(searchString) {
  if (searchString) { return getData("/appointments", formatResponse_PopulateTable, {search: searchString}); }
  getData("/appointments", formatResponse_PopulateTable);
}

function showAddForm() {
  appointmentForm.show();
  addBtn.show();
  newBtn.hide();
}

function onInit_setDefaults(callback) {
  !addBtn && (addBtn = $("#addAppointmentBtn"));
  !appointmentForm && (appointmentForm = $("#appointmentForm"));
  if (!newBtn) {
    newBtn = $("#newAppointmentBtn");
    newBtn.click(function () {
      showAddForm();
    });
  }

  addBtn.hide();
  appointmentForm.hide();
  newBtn.show();

  callback && (callback());
}

function checkAddForm(form) {
  // regular expression to match required date format
  var re = /^\d{4}\-\d{1,2}\-\d{1,2}$/;

  if (form.newAppointmentDate.value != '' && !form.newAppointmentDate.value.match(re)) {
    alert("Invalid date format: " + form.newAppointmentDate.value);
    form.newAppointmentDate.focus();
    return false;
  }
  return true;
}

function submitSearchForm() {
  var string = $( "#searchFormText" ).val();

  if (string && string !== "" ) {
    return getAppointments(string);
  }

  getAppointments();
}

$(function() {
  onInit_setDefaults(function() {
    $("#cancelAppointmentBtn").click(function () {
      onInit_setDefaults();
    });

    getAppointments();
  });

});
