$(".go").click(function(){
    $('#user-info').removeAttr('class').addClass('form-info');
    $('#date').removeAttr('class');
    $('.go').attr('id', 'button-vis');
    $('input[name="next-step"]').removeAttr('id');
    $('.back').removeAttr('id');

});
$(".back").click(function(){
    $('#date').removeAttr('class').addClass('form-info');
    $('#user-info').removeAttr('class');
    // $('#next-step').hide();
    var input = $('<div>Продолжить</div>').addClass('go').attr('id', 'go');
    $('#next-step').replaceWith(input);
    $('.go').removeAttr('id');
    $('input[name="next-step"]').attr('id', 'button-vis');
    $('.back').attr('id', 'button-vis');
  });
  
