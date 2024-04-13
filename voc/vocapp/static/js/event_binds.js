

const EventsBindener = {

	hp_page_list_PagesHomePageDeleteButton: function() {
		RemovePage($('#id_pages_ul_group').find(':selected').data(`page_id`), $('#id_pages_ul_group').find(':selected').val());
		FillPagesEdit();
	},

	hp_pages_list_PagesHomePageEditButton: function() {
		RunInScreenForm({form_name:`page_edit`,
		execute_after_load:`FillEditPageForm();ResizeModalForms();`,
		request_link:`/hp_edit_page/`+$('#id_pages_ul_group').find(':selected').data(`page_id`),
		execute_on_ok:'',
		execute_on_close:'FillPagesEdit();'});
	},

	hp_pages_list_AddButton: function() {
		RunInScreenForm({  form_name:`page_edit`,
		execute_after_load:`FillEditPageForm(); ResizeModalForms();`,
		request_link:`/hp_edit_page/0`,
		execute_on_ok:'',
		execute_on_close:'FillPagesEdit();'});
	},


	hp_page_edit_DeleteRowButton: function() {
		RemoveRowFromPage(
			document.querySelector(`#row_name_${document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id}`).textContent,
			document.querySelector(`#page_edit_data_container`).dataset.page_id,
			document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id
		);
	},

	hp_page_edit_MoveDownButton: function() {
		MoveInPageRow({
			direction:  'down',
			page_id:    document.querySelector(`#page_edit_data_container`).dataset.page_id,
			row_id:     document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id
		  })	},

	hp_page_edit_MoveUpButton: function() {
		MoveInPageRow({
			direction:  'up',
			page_id:     document.querySelector(`#page_edit_data_container`).dataset.page_id,
			row_id:      document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id
		  });
	},

	hp_page_edit_EditButton: function() {
		console.log('===**====');
		console.log(document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id);
		RunInScreenForm({form_name:`page_edit`,
									execute_after_load:`FillEditRowForm();ResizeModalForms();`,
									request_link:`/hp_edit_row/`+document.querySelector(`#row_list[data-selected='yes']`).dataset.row_id,
									execute_on_ok:'',
									execute_on_close:'FillEditPageForm();'});
	},

	hp_page_edit_add_button: function() {
		RunInScreenForm({  form_name:`rows_edit`,
		execute_after_load:`  
							  (async () => { {eval('FillRowsEdit();')} })();
							  ResizeModalForms();
							  document.querySelector('#hp_rows_list_RowsHomePageSelectButton').style.display = "block";
							  RefreshElementsEditRowForm();
							;`,
		request_link:`/hp_edit_rows/`});
	},

	hp_rows_list_RowsHomePageSelectButton: function() {
		//add row into page
		AddRowIntoPage(
				GetSelectedHomeRowId(), //row_id
				GetSelectedHomePagePageId()//page_id
			);
		CloseToplevelDynamicForm();
	},


	hp_row_edit_id_save_row: function() {
		SaveRow(document.querySelector('#hp_row_edit_id_save_row').dataset.row_id,  document.querySelector('#inputRowName').value);
		CloseToplevelDynamicForm();
    },

	hp_row_edit_id_cancel_row: function() {
		CloseToplevelDynamicForm();
    },




	hp_rows_list_RowsHomePageAddButton: function() {
		RunInScreenForm({   form_name:`row_edit`,
		execute_after_load:`FillEditRowForm();ResizeModalForms();`,
		request_link:`/hp_edit_row/0`,
		execute_on_ok:'',
		execute_on_close:''
	});
    },

	hp_rows_list_closeButton: function() {
		CloseToplevelDynamicForm();
    },
	
	hp_rows_list_RowsHomePageDeleteButton: function() {
        RemoveRow($('#id_rows_list').find(':selected').data('row_id'), $('#id_rows_list').find(':selected').val());
    },

    hp_rows_list_RowsHomePageEditButton: function() {
        RunInScreenForm({
            form_name: 'row_edit',
            execute_after_load: 'FillEditRowForm();ResizeModalForms();',
            request_link: '/hp_edit_row/' + $('#id_rows_list').find(':selected').data('row_id'),
            execute_on_ok: '',
            execute_on_close: 'FillRowsEdit();'
        });
    },








    assignOnClickToMatchingElement: function() {
        for (let methodName in this) {
            if (typeof this[methodName] === 'function') {
                const element = document.getElementById(methodName);
                if (element) {
                    element.onclick = this[methodName].bind(this);
                }
            }
        }
    }
};

