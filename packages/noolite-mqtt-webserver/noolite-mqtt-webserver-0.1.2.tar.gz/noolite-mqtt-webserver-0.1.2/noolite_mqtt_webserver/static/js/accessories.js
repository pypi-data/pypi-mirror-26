(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);


var accessoryDelete = function (accessory_name) {
  $.ajax({
    url: '/accessory/' + accessory_name,
    type: 'DELETE',
    success: function (data) {
      $('#accessory_' + accessory_name).remove();
    }
  })
};


$("#accessoryCreate").submit(function(e) {
    var form = this;
    $('button', this).prop('disabled', true);

    var formData = $(this).serializeFormJSON();
    var url = "/accessory";

    $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(formData),
        success: function(data)
        {
            location.reload();
        },
        complete: function (data) {
            $('button', form).prop('disabled', false);
        }
    });

    e.preventDefault();
});


$("#accessoryDelete").submit(function(e) {
    var form = this;
    $('button', this).prop('disabled', true);

    var url = "/accessory/" + this.name.value;

    $.ajax({
        type: "DELETE",
        url: url,
        success: function(data)
        {
            $(form)[0].name.value = '';
        },
        complete: function (data) {
            $('button', form).prop('disabled', false);
        }
    });

    e.preventDefault();
});