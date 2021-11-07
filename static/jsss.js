// $(document).ready(function() {
//     $("#submitBtn").click(function() {
//         $("#myForm").submit(); // Submit the form
//     });
// });


function refresh() {
    $.ajax({
        url: "",
        dataType: "text",
        success: function(html) {
            $('#fu').replaceWith($.parseHTML(html));
            setTimeout(refresh, 2000);
        }
    });
}