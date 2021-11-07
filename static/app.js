$(document).ready(function() {

    $('.updateButton').on('click', function() {


        var name = $('#nameInput').val();


        req = $.ajax({
            url: "{{url_for('admin')}}",
            type: 'POST',
            data: { name: name }
        });

        req.done(function(data) {
            for (let dat in data) {

                $('fi' + employee[0]).text(dat.employee[0]);
                $('se' + employee[1]).text(dat.employee[1]);
                $('th' + employee[2]).text(dat.employee[2]);


            }


        });


    });

});