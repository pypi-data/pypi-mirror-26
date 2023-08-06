$('#request_form').submit(function (e) {
  $('#request_status').html('');

  $.get('/api.htm', $('#request_form').serialize())
    .done(function (data) {
      if (data.usb_response.length > 0) {

        $.each(data.usb_response, function (index, response_item) {
          var tr_string = '<td>' + (index + 1) +'</td>';

          $.each(response_item, function (index, byte) {
            tr_string += '<td>' + byte + '</td>'
          });

          $('#response_table_body').append('<tr>' + tr_string + '</tr>')
        });

        $('#request_status').removeClass('label-warning').addClass('label-success').html('Ответ получен');
      } else {
        $('#request_status').removeClass('label-success').addClass('label-warning').html('Нет ответа');
      }
    });

  e.preventDefault();
});


var clear_response_table = function () {
  $('#response_table_body').html('')
};