window.addEventListener('load', function () {
    // 定义判断函数
    let emtpy_validate = function (element) {
        return element.value;
    };
    let float_validate = function (element) {
        let min = parseFloat(element.getAttribute('min'));
        let max = parseFloat(element.getAttribute('max'));
        let value = parseFloat(element.value);
        return /^[0-9]+\.[0-9]{0,5}$/.test(element.value) && value >= min && value <= max;
    };
    let integer_validate = function (element) {
        let min = parseInt(element.getAttribute('min'));
        let max = parseInt(element.getAttribute('max'));
        let value = parseInt(element.value);
        return /^[0-9]+$/.test(element.value) && value >= min && value <= max;
    };

    // 获取元素
    let $model = document.querySelector('select[name=\'model\']');
    let $optimizer = document.querySelector('select[name=\'optimizer\']');
    let $learning_rate = document.querySelector('input[name=\'learning_rate\']');
    let $batch_size = document.querySelector('input[name=\'batch_size\']');
    let $epochs = document.querySelector('input[name=\'epochs\']');
    let $task = document.querySelector('input[name=\'task\']');
    let $person = document.querySelector('input[name=\'person\']');

    // 每个元素设置监听
    let form_select_empty_validate_elements = [$model, $optimizer];
    let form_control_empty_validate_elements = [$task, $person];
    let form_control_empty_float_validate_elements = [$learning_rate];
    let form_control_empty_integer_validate_elements = [$batch_size, $epochs];

    for (let element of form_select_empty_validate_elements) {
        element.addEventListener('change', function () {
            if (emtpy_validate(element)) {
                element.className = 'form-select is-valid';
            } else {
                element.className = 'form-select is-invalid';
            }
        });
    }

    for (let element of form_control_empty_validate_elements) {
        element.addEventListener('change', function () {
            if (emtpy_validate(element)) {
                element.className = 'form-control is-valid';
            } else {
                element.className = 'form-control is-invalid';
            }
        });
    }

    for (let element of form_control_empty_float_validate_elements) {
        element.addEventListener('change', function () {
            if (emtpy_validate(element) && float_validate(element)) {
                element.className = 'form-control is-valid';
            } else {
                element.className = 'form-control is-invalid';
            }
        });
    }

    for (let element of form_control_empty_integer_validate_elements) {
        element.addEventListener('change', function () {
            if (emtpy_validate(element) && integer_validate(element)) {
                element.className = 'form-control is-valid';
            } else {
                element.className = 'form-control is-invalid';
            }
        });
    }

    // 表单提交
    let $form = document.querySelector('form');
    $form.addEventListener('submit', function (e) {
        let can_submit = true;
        for (let element of form_select_empty_validate_elements) {
            element.dispatchEvent(new Event('change'));
            if (!emtpy_validate(element)) {
                can_submit = false;
            }
        }
        for (let element of form_control_empty_validate_elements) {
            element.dispatchEvent(new Event('change'));
            if (!emtpy_validate(element)) {
                can_submit = false;
            }
        }
        for (let element of form_control_empty_float_validate_elements) {
            element.dispatchEvent(new Event('change'));
            if (!emtpy_validate(element) || !float_validate(element)) {
                can_submit = false;
            }
        }
        for (let element of form_control_empty_integer_validate_elements) {
            element.dispatchEvent(new Event('change'));
            if (!emtpy_validate(element) || !integer_validate(element)) {
                can_submit = false;
            }
        }
        if (!can_submit) {
            e.preventDefault();
        } else {
            setTimeout(() => alert('模型开始训练！'), 100);
        }
    });
});