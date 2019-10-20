
//wakeup
$(function () {
    'use strict';
    $('#wakeup').fileupload({
        url: '/wakeup'
    });

    $('#wakeup').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    if (window.location.hostname === 'blueimp.github.io') {
        $('#wakeup').fileupload('option', {
            url: '//jquery-file-upload.resultspot.com/',
            disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
        });
        if ($.support.cors) {
            $.ajax({
                url: '//jquery-file-upload.resultspot.com/',
                type: 'HEAD'
            }).fail(function () {
                $('<div class="alert alert-danger"/>')
                    .text('Upload server currently unavailable - ' +
                            new Date())
                    .resultendTo('#fileupload');
            });
        }
    } else {
        // Load existing files:
        $('#wakeup').addClass('fileupload-processing');
        $.ajax({
            url: $('#wakeup').fileupload('option', 'url'),
            dataType: 'json',
            context: $('#wakeup')[0]
        }).always(function () {
            $(this).removeClass('fileupload-processing');
        }).done(function (result) {
            $(this).fileupload('option', 'done')
                .call(this, $.Event('done'), {result: result});
        });
    }
});


// plot
$(function () {
    'use strict';
    $('#nowakeup').fileupload({
        url: '/plotFile'
    });

    $('#nowakeup').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    if (window.location.hostname === 'blueimp.github.io') {
        $('#nowakeup').fileupload('option', {
            url: '//jquery-file-upload.resultspot.com/',
            disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
        });
        if ($.support.cors) {
            $.ajax({
                url: '//jquery-file-upload.resultspot.com/',
                type: 'HEAD'
            }).fail(function () {
                $('<div class="alert alert-danger"/>')
                    .text('Upload server currently unavailable - ' +
                            new Date())
                    .resultendTo('#fileupload');
            });
        }
    } else {
        // Load existing files:
        $('#nowakeup').addClass('fileupload-processing');
        $.ajax({
            url: $('#nowakeup').fileupload('option', 'url'),
            dataType: 'json',
            context: $('#nowakeup')[0]
        }).always(function () {
            $(this).removeClass('fileupload-processing');
        }).done(function (result) {
            $(this).fileupload('option', 'done')
                .call(this, $.Event('done'), {result: result});
        });
    }
});

// vad
$(function () {
    'use strict';
    $('#vad_test').fileupload({
        url: '/vadFile'
    });

    $('#vad_test').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    if (window.location.hostname === 'blueimp.github.io') {
        $('#vad_test').fileupload('option', {
            url: '//jquery-file-upload.resultspot.com/',
            disableImageResize: /Android(?!.*Chrome)|Opera/
                .test(window.navigator.userAgent),
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i
        });
        if ($.support.cors) {
            $.ajax({
                url: '//jquery-file-upload.resultspot.com/',
                type: 'HEAD'
            }).fail(function () {
                $('<div class="alert alert-danger"/>')
                    .text('Upload server currently unavailable - ' +
                            new Date())
                    .resultendTo('#fileupload');
            });
        }
    } else {
        // Load existing files:
        $('#vad_test').addClass('fileupload-processing');
        $.ajax({
            url: $('#vad_test').fileupload('option', 'url'),
            dataType: 'json',
            context: $('#vad_test')[0]
        }).always(function () {
            $(this).removeClass('fileupload-processing');
        }).done(function (result) {
            $(this).fileupload('option', 'done')
                .call(this, $.Event('done'), {result: result});
        });
    }
});
