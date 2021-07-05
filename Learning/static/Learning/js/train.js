window.addEventListener('load', function () {
    let $form = document.querySelector('form');
    $form.addEventListener('submit', function (e) {
        let $model = document.querySelector('select[name=\'model\']');
        let $optimizer = document.querySelector('select[name=\'optimizer\']');
        let $learning_rate = document.querySelector('input[name=\'learning_rate\']');
        let $batch_size = document.querySelector('input[name=\'batch_size\']');
        let $epochs = document.querySelector('input[name=\'epochs\']');
        let $task = document.querySelector('input[name=\'task\']');
        let $person = document.querySelector('input[name=\'person\']');
        let form_select_empty_validate_items = [$model, $optimizer];
        let form_control_empty_validate_items = [$learning_rate, $batch_size, $epochs, $task, $person];
        let form_control_float_range_validate_items = [$learning_rate];
        let form_control_integer_range_validate_items = [$batch_size, $epochs];
        let can_submit = true;
        for (let item of form_select_empty_validate_items) {
            if (item.value) {
                item.className = 'form-select is-valid';
            } else {
                item.className = 'form-select is-invalid';
                can_submit = false;
            }
        }
        for (let item of form_control_empty_validate_items) {
            if (item.value) {
                item.className = 'form-control is-valid';
            } else {
                item.className = 'form-control is-invalid';
                can_submit = false;
            }
        }
        for (let item of form_control_float_range_validate_items) {
            let min = parseFloat(item.getAttribute('min'));
            let max = parseFloat(item.getAttribute('max'));
            let value = parseFloat(item.value);
            if (/^[0-9]+\.[0-9]{0,5}$/.test(item.value) && value >= min && value <= max) {
                item.className = 'form-control is-valid';
            } else {
                item.className = 'form-control is-invalid';
                can_submit = false;
            }
        }
        for (let item of form_control_integer_range_validate_items) {
            let min = parseInt(item.getAttribute('min'));
            let max = parseInt(item.getAttribute('max'));
            let value = parseInt(item.value);
            if (/^[0-9]+$/.test(item.value) && value >= min && value <= max) {
                item.className = 'form-control is-valid';
            } else {
                item.className = 'form-control is-invalid';
                can_submit = false;
            }
        }
        if (!can_submit) {
            e.preventDefault();
        } else {
            alert('模型开始训练！');
        }
    });
});