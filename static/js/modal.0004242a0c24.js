$(".testimonial-name").click(function(){
  var buttonId = $(this).attr('id');
  $('#modal-container').removeAttr('class').addClass(buttonId);
  $('#date').removeAttr('class').addClass('form-info');
  $('#user-info').removeAttr('class');
  $('input[name="next-step"]').attr('id', 'button-vis');
  $('.back').attr('id', 'button-vis');
  $('.go').removeAttr('id');
});

$('body').click(function(event){
const ignoreElements = ["modal-container", "buttons", "modal", "go", "navbtn", "back", "flatpickr-calendar", "testimonial-name", "shadow-effect", "item"];
let pass = true;

$(ignoreElements).each(function(key, value) {
  if ($(event.target).hasClass(value) || $(event.target).closest(`.${value}`).length > 0) {
    pass = false;
  }
});

if (pass) {
  var buttonId = $(this).attr('id');
  $('#modal-container').addClass("out");
}
});

// $(function() {
//   $('.button').on("click", function(e) {
//     var buttonId = $(this).attr('id');
//     $('#modal-container').removeAttr('class').addClass(buttonId);
//   });
//   $(document).on("click", function(e) {
//     var buttonId = $(this).attr('id');
//     if ($(e.target).is("#modal-container, #user-login-top") === false) {
//       $('#modal-container').removeClass(buttonId);
//     }
//   });
// });