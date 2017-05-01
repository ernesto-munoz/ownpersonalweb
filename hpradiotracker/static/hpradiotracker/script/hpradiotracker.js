$(document).ready(function(){

    // Login Button Action
    $("#login-button").click(function(event){
        event.preventDefault()
        var username = $('#login-username').val()
        var password = $('#login-password').val()
        $.post(
            'login',
            {
                'login-username': username,
                'login-password': password
            },
            function(data){
                if(data.valid_login == true){
                    location.reload(true)
                }else{
                    $("p#error-paragraph").text(data.message)
                    $("p#error-paragraph").addClass('text-danger')
                }
            }
        )
    });

    // Update Database Button
    $("#update-database-button").click(function(){
        $(this).html('Updating...')
        var how_many_pages = $("select#select-update-depth").val()
        $(this).prop('disabled', true)
        $.post(
            'update_radio_database',
            {
                'how_many_pages': how_many_pages
            },
            function(data){
                location.reload(true)
            }
        )
    });

    // Button to change between seen and not seen
    $(".link-change-seen").click(function(){
        var identifier = $(this).attr('id').split('-')[3]
        var $this = $(this)
        $.post(
            'change_seen',
            { 'inner_identifier': identifier },
            function(data){
                $this.find('img').attr('src', data.new_image_url)
            }
        )
    });

    // Launch the download of the file for the loged user in the server
    $(".link-download-file").click(function(){
        console.log('Download file link')
        $("p#message-paragraph").text("The file is being downloaded in the server. Please, be patient.")
        $("p#message-paragraph").addClass("text-info")
        var identifier = $(this).attr('id').split('-')[3]
        var $this = $(this)
        // remove the color in the row that isn't going to be the file downloaded
        $("tr.file-downloaded").removeClass("bg-success file-downloaded")
        // for safety, delete src of the audio player
        $("audio#audio-controler").attr("src", "")
        $.post(
            'download_file',
            { 'inner_identifier': identifier },
            function(data){
                // message info
                $("p#message-paragraph").text(data.message)
                $("p#message-paragraph").removeClass("text-info")
                $("p#message-paragraph").addClass("text-success")
                // add color an the file-downloaded class to the row
                $("tr#row-program-" + identifier).addClass("bg-success file-downloaded")
            }
        )
    });

    // Load the file in the audio-controler
    $("#play-button").click(function(event){
        event.preventDefault()
        var $this = $(this)
        $.post(
            'get_play_file_url',
            {},
            function(data){
                $("audio#audio-controler").attr("src", data.audio_url)
                $("audio#audio-controler")[0].play()
            }
        )
    });

    // Search for a query_string in the database
    $("#search-button").click(function(event){
        event.preventDefault()
        var $this = $(this)
        var query_string = $("#query-string").val()
        var page = Number($("ul.pagination.active#span-data").val())
        $.post(
            'get_radio_table_html',
            {
                'page': page,
                'query_string': query_string
            },
            function(data){
                $("#general-div-radio-table").remove()
                $("#table-content").append(data.rendered)
            }
        )
    });

    /* To allow to send ajax post query with the csrf protection
    https://docs.djangoproject.com/en/1.11/ref/csrf/
    */
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    /* CSRF Protection End */
});
