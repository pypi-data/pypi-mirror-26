$(document).on('change', '.show-selected-icon select', function(){
	var parent = $(this).parent().parent();
	if ($(this).val()) {
		if (parent.children('.selected-icon').length == 0) {
			parent.append('<div class="selected-icon"><p class="help">Gekozen icoon: <i class="fa fa-' + $(this).val() + '"></i></p></div>');
		} else {
			parent.find('.selected-icon i').removeAttr('class').addClass('fa fa-' + $(this).val());
		}		
	} else {
		parent.children('.selected-icon').remove();
	}
});

$(document).on('change', '.show-selected-color select', function(){
	var parent = $(this).parent().parent();
	if ($(this).val()) {
		if (parent.children('.selected-color').length == 0) {
			parent.append('<div class="selected-color"><p>Gekozen kleur: </p><span class="' + $(this).val() + '"></span></div>');
		} else {
			parent.find('.selected-color span').removeAttr('class').addClass($(this).val());
		}		
	} else {
		parent.children('.selected-color').remove();
	}
});


/*
var button, div;

$(document).on('hidden.bs.modal', '.modal:first', function (e) {
	div = button.closest('div.sequence-container-inner');
	div.children('button:last').click();
	div.find('.button.action-choose.button-small.button-secondary:last').trigger('click');
});


$(document).on('click', '.button.action-choose', function() {
	button = $(this);
});

*/


$(document).ready(function(){

	$(document).on('change', 'li.formbuilder-type select[name$="field_type"]', function(){
		var option = $(this).val();
		// checkboxes, radiobuttons en dropdowns.
		$(this).closest('li.formbuilder-type').next('li').hide();
		$(this).closest('li.formbuilder-type').siblings('.integer_field').hide();

		if (option == 'checkbox' || option == 'checkboxes' || option == 'radio' || option == 'dropdown') {
			$(this).closest('li.formbuilder-type').next('li').show();
		} else if (option == 'singleline') { 
			$(this).closest('li.formbuilder-type').siblings('.integer_field').show();
		}
	});
	$('li.formbuilder-type select[name$="field_type"]').trigger('change');

	if (collapse) {
		$.each($('.sequence:has(.grid-title):first > li'), function(){
			var titles = [];
			$.each($(this).find('.grid-title'), function(){
				width = $(this).parent().next().find('select option[selected]').text();
				if (width == '---------') {
					width = '*';
				}
				titles.push($(this).find('input[type=text]:first').val() + '[' + width + ']' ); 
			});
			$(this).find('.sequence-type-list > .sequence-container-inner:first').prepend('<span style="font-size:20px;text-transform:uppercase;clear:both;">' + titles.join(', ') + '</span>');
		});

		var collapsebutton = '<button type="button" title="Collapse" id="body-0-value-0-collapse" class="button icon text-replace hover-no icon-cross toggle-button">Collapse</button>';

		$('.grid-title').closest('.sequence-member-inner').prev().append(collapsebutton);
		$('.sequence:has(.grid-title) > li > .sequence-controls > .button-group').append(collapsebutton);

		$(document).on('click', '.toggle-button', function(){
			$(this).closest('.sequence-member').toggleClass('hiddenchildren');
			$(this).toggleClass('icon-cross').toggleClass('icon-plus');
			$(this).closest('.sequence-controls').next().find('button:last').toggleClass('hidden')
		});

		setTimeout(function(){
			$('.toggle-button').trigger('click');

			// if errors open again...
			$('.sequence:has(.grid-title):first > li:has(.error-message) .toggle-button').trigger('click');
		}, 10);
		
		
	}
});

