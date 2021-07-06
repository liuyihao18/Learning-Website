window.addEventListener('load', function () {
    let $delete = document.getElementsByClassName('delete-operate');
    for (let element of $delete) {
        element.addEventListener('click', (e) => {
            if (!confirm('确定删除？')) {
                e.preventDefault();
            }
        });
    }
});