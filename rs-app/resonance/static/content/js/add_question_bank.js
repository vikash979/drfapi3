// mask input function start
function mask_decrease(){
  var mask_input_value = parseInt($('input[name="mask"]').val());
  if (mask_input_value > 0 && mask_input_value != 0) {
    append_mask_input_value = --mask_input_value;
    $('input[name="mask"]').val(append_mask_input_value);
  }
}
function mask_increment(){
  var mask_input_value = parseInt($('input[name="mask"]').val());
  append_mask_input_value = ++mask_input_value;
  $('input[name="mask"]').val(append_mask_input_value);
}

// negative mask function start
function negative_mask_decrease(){
  var negative_mask_decrease_value = $('input[name="negative-mark"]').val();
  append_negative_mask_decrease_value = --negative_mask_decrease_value;
  $('input[name="negative-mark"]').val(append_negative_mask_decrease_value);
}

function negative_mask_increment(){
  var negative_mask_decrease_value = $('input[name="negative-mark"]').val();
  append_negative_mask_decrease_value = ++negative_mask_decrease_value;
  if (append_negative_mask_decrease_value <= 0) {
    $('input[name="negative-mark"]').val(append_negative_mask_decrease_value);
  }
}

// time duration function start
function duration_decrease(){
  var duration_value = parseInt($('input[name="duration"]').val());
  if (duration_value > 0 && duration_value != 0) {
    var append_duration_value = --duration_value;
    $('input[name="duration"]').val(append_duration_value);
  }
}

function duration_increment(){
  var duration_value = parseInt($('input[name="duration"]').val());
  var append_duration_value = ++duration_value;
  $('input[name="duration"]').val(append_duration_value);
}

var question_type_dict = {1: 'Multiple Choice Questions', 2: 'Single Integer Questions', 3: 'Multiple Response Questions', 4: 'Fill in the Blanks', 5: 'True False', 6: 'Subjective'}

var multi_response_question = `
            <li id="parent">
                <i>1</i>
                <div><input type="text" name="option" placeholder="Typing Options" required></div>
                <li id="true_false_option">
                    <a href="javascript:void(0);">True</a>
                </li>
            </li>`

var true_false_question = `
            <li id="parent">
                <i>1</i>
                <div><input type="text" name="option" value="True" readonly></div>
                <li id="true_false_option">
                    <a href="javascript:void(0);">True</a>
                </li>
            </li>
            <li id="parent">
                <i>2</i>
                <div><input type="text" name="option" value="False" readonly></div>
                <li id="true_false_option">
                    <a href="javascript:void(0);">True</a>
                </li>
            </li>`

function delete_all_parent_elements(){
  $('li#parent').each(function(){
    $(this).remove();
  });
  $('li#true_false_option').each(function(){
    $(this).remove();
  })
}

function question_type_change_value(){
  if ($('select[name="question_type"]').val() == 3) {
    delete_all_parent_elements();
    $('#option').append(multi_response_question);
    $('.add-optn-btn').css('display', 'flex');
  } else if ($('select[name="question_type"]').val() == 5) {
    delete_all_parent_elements();
    $('.add-optn-btn').css('display', 'none');
    $('#option').append(true_false_question);
  }
};

function add_question_option(){
  var option_value_length = parseInt($('#option li').not('#true_false_option').length);
  var next_append_value = ++option_value_length;
  option_data = `
  <li id="parent">
      <i>${next_append_value}</i>
      <div><input type="text" name="option" placeholder="Typing Options" required></div>
      <li id="true_false_option">
          <a href="javascript:void(0);">True</a>
      </li>
  </li>`
  $('#option').append(option_data);
}

function true_false_option(){
  $(document).on('click', '#true_false_option a', function(e){
    var clickElement = e.target;
    $('#true_false_option a.active').removeAttr('class', 'active');
    clickElement.setAttribute('class','active');
    var get_true_value = e.target.parentNode.previousSibling.innerText;
    $('#option_true_value').val(get_true_value);
  });
}

$(window).on('load', function(){
  true_false_option();
})
