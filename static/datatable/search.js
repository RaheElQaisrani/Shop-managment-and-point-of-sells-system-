$(document).ready(function() {
    $('#search-input').select2({
        ajax: {
            url: '/search',
            dataType: 'json',
            data: function (params) {
                return {
                    term: params.term,
                    search_by: $('#search-by-select').val()
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
            cache: true
        },
        placeholder: 'Search by...',
        minimumInputLength: 1
    });

    // When the search by select box changes, update the search bar placeholder text
    $('#search-by-select').on('change', function() {
        var selectedOption = $('#search-by-select option:selected').text();
        $('#search-input').attr('placeholder', 'Search by ' + selectedOption.toLowerCase() + '...');
    });

    // Navigate to the appropriate update route when a product is selected
    $('#search-input').on('select2:select', function (e) {
        var data = e.params.data;
        window.location.href = `/update/${data.id}`;
    });
});
