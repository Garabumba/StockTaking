$("#vendor-filter-icon").click(function() {
    $("#vendor-filter-dropdown").toggle();
});

$("#vendor-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#vendor-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#vendor-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='vendor']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#vendor-filter-icon, #vendor-filter-dropdown").length) {
        $("#vendor-filter-dropdown").hide();
    }
});

$("#model-filter-icon").click(function() {
    $("#model-filter-dropdown").toggle();
});

$("#model-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#model-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#model-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='model']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#model-filter-icon, #model-filter-dropdown").length) {
        $("#model-filter-dropdown").hide();
    }
});

$("#canInstalling-filter-icon").click(function() {
    $("#canInstalling-filter-dropdown").toggle();
});

$("#canInstalling-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#canInstalling-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#canInstalling-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='can_installing']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#canInstalling-filter-icon, #canInstalling-filter-dropdown").length) {
        $("#canInstalling-filter-dropdown").hide();
    }
});

$("#isUpdating-filter-icon").click(function() {
    $("#isUpdating-filter-dropdown").toggle();
});

$("#isUpdating-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#isUpdating-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#isUpdating-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='is_updating']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#isUpdating-filter-icon, #isUpdating-filter-dropdown").length) {
        $("#isUpdating-filter-dropdown").hide();
    }
});

$("#cores-filter-icon").click(function() {
    $("#cores-filter-dropdown").toggle();
});

$("#cores-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#cores-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#cores-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='cores']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#cores-filter-icon, #cores-filter-dropdown").length) {
        $("#cores-filter-dropdown").hide();
    }
});

$("#threads-filter-icon").click(function() {
    $("#threads-filter-dropdown").toggle();
});

$("#threads-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#threads-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#threads-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='threads']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#threads-filter-icon, #threads-filter-dropdown").length) {
        $("#threads-filter-dropdown").hide();
    }
});

$("#frequency-filter-icon").click(function() {
    $("#frequency-filter-dropdown").toggle();
});

$("#frequency-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#frequency-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#frequency-list li").click(function() {
    var value = $(this).data("value");
    
    $("form[id^='filter-form'] select[name='frequency']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#frequency-filter-icon, #frequency-filter-dropdown").length) {
        $("#frequency-filter-dropdown").hide();
    }
});

$("#type-filter-icon").click(function() {
    $("#type-filter-dropdown").toggle();
});

$("#type-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#type-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#type-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='type']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#type-filter-icon, #type-filter-dropdown").length) {
        $("#type-filter-dropdown").hide();
    }
});

$("#serialNumber-filter-icon").click(function() {
    $("#serialNumber-filter-dropdown").toggle();
});

$("#serialNumber-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#serialNumber-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#serialNumber-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='serial_number']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#serialNumber-filter-icon, #serialNumber-filter-dropdown").length) {
        $("#serialNumber-filter-dropdown").hide();
    }
});

$("#memory-filter-icon").click(function() {
    $("#memory-filter-dropdown").toggle();
});

$("#memory-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#memory-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#memory-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='memory']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#memory-filter-icon, #memory-filter-dropdown").length) {
        $("#memory-filter-dropdown").hide();
    }
});

$("#inventoryNumber-filter-icon").click(function() {
    $("#inventoryNumber-filter-dropdown").toggle();
});

$("#inventoryNumber-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#inventoryNumber-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#inventoryNumber-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='inventory_number']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#inventoryNumber-filter-icon, #inventoryNumber-filter-dropdown").length) {
        $("#inventoryNumber-filter-dropdown").hide();
    }
});

$("#resolution-filter-icon").click(function() {
    $("#resolution-filter-dropdown").toggle();
});

$("#resolution-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#resolution-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#resolution-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='resolution']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#resolution-filter-icon, #resolution-filter-dropdown").length) {
        $("#resolution-filter-dropdown").hide();
    }
});

$("#resolutionFormat-filter-icon").click(function() {
    $("#resolutionFormat-filter-dropdown").toggle();
});

$("#resolutionFormat-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#resolutionFormat-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#resolutionFormat-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='resolution_format']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#resolutionFormat-filter-icon, #resolutionFormat-filter-dropdown").length) {
        $("#resolutionFormat-filter-dropdown").hide();
    }
});

$("#universityBody-filter-icon").click(function() {
    $("#universityBody-filter-dropdown").toggle();
});

$("#universityBody-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#universityBody-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#universityBody-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='university_body']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#universityBody-filter-icon, #universityBody-filter-dropdown").length) {
        $("#universityBody-filter-dropdown").hide();
    }
});

$("#maxComputers-filter-icon").click(function() {
    $("#maxComputers-filter-dropdown").toggle();
});

$("#maxComputers-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#maxComputers-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#maxComputers-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='max_computers']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#maxComputers-filter-icon, #maxComputers-filter-dropdown").length) {
        $("#maxComputers-filter-dropdown").hide();
    }
});

$("#maxPlaces-filter-icon").click(function() {
    $("#maxPlaces-filter-dropdown").toggle();
});

$("#maxPlaces-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#maxPlaces-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#maxPlaces-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='max_places']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#maxPlaces-filter-icon, #maxPlaces-filter-dropdown").length) {
        $("#maxPlaces-filter-dropdown").hide();
    }
});

$("#colorPrinting-filter-icon").click(function() {
    $("#colorPrinting-filter-dropdown").toggle();
});

$("#colorPrinting-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#colorPrinting-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#colorPrinting-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='color_printing']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#colorPrinting-filter-icon, #colorPrinting-filter-dropdown").length) {
        $("#colorPrinting-filter-dropdown").hide();
    }
});

$("#printType-filter-icon").click(function() {
    $("#printType-filter-dropdown").toggle();
});

$("#printType-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#printType-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#printType-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='print_type']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#printType-filter-icon, #printType-filter-dropdown").length) {
        $("#printType-filter-dropdown").hide();
    }
});

$("#status-filter-icon").click(function() {
    $("#status-filter-dropdown").toggle();
});

$("#status-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#status-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#status-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='status']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#status-filter-icon, #status-filter-dropdown").length) {
        $("#status-filter-dropdown").hide();
    }
});

$("#isNetworking-filter-icon").click(function() {
    $("#isNetworking-filter-dropdown").toggle();
});

$("#isNetworking-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#isNetworking-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#isNetworking-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='is_networking']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#isNetworking-filter-icon, #isNetworking-filter-dropdown").length) {
        $("#isNetworking-filter-dropdown").hide();
    }
});

$("#yearOfProduction-filter-icon").click(function() {
    $("#yearOfProduction-filter-dropdown").toggle();
});

$("#yearOfProduction-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#yearOfProduction-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#yearOfProduction-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='year_of_production']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#yearOfProduction-filter-icon, #yearOfProduction-filter-dropdown").length) {
        $("#yearOfProduction-filter-dropdown").hide();
    }
});

$("#withRemoteController-filter-icon").click(function() {
    $("#withRemoteController-filter-dropdown").toggle();
});

$("#withRemoteController-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#withRemoteController-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#withRemoteController-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='with_remote_controller']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#withRemoteController-filter-icon, #withRemoteController-filter-dropdown").length) {
        $("#withRemoteController-filter-dropdown").hide();
    }
});

$("#audience-filter-icon").click(function() {
    $("#audience-filter-dropdown").toggle();
});

$("#audience-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#audience-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#audience-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='audience']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#audience-filter-icon, #audience-filter-dropdown").length) {
        $("#audience-filter-dropdown").hide();
    }
});

$("#diagonal-filter-icon").click(function() {
    $("#diagonal-filter-dropdown").toggle();
});

$("#diagonal-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#diagonal-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#diagonal-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='diagonal']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#diagonal-filter-icon, #diagonal-filter-dropdown").length) {
        $("#diagonal-filter-dropdown").hide();
    }
});

$("#ip-filter-icon").click(function() {
    $("#ip-filter-dropdown").toggle();
});

$("#ip-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#ip-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#ip-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='ip']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#ip-filter-icon, #ip-filter-dropdown").length) {
        $("#ip-filter-dropdown").hide();
    }
});

$("#arch-filter-icon").click(function() {
    $("#arch-filter-dropdown").toggle();
});

$("#arch-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#arch-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#arch-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='arch']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#arch-filter-icon, #arch-filter-dropdown").length) {
        $("#arch-filter-dropdown").hide();
    }
});

$("#name-filter-icon").click(function() {
    $("#name-filter-dropdown").toggle();
});

$("#name-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#name-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#name-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='name']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#name-filter-icon, #name-filter-dropdown").length) {
        $("#name-filter-dropdown").hide();
    }
});

$("#aspectRatio-filter-icon").click(function() {
    $("#aspectRatio-filter-dropdown").toggle();
});

$("#aspectRatio-search").keyup(function() {
    var filter = $(this).val().toLowerCase();
    $("#aspectRatio-list li").each(function() {
        var text = $(this).text().toLowerCase();
        $(this).toggle(text.includes(filter));
    });
});

$("#aspectRatio-list li").click(function() {
    var value = $(this).data("value");
    $("form[id^='filter-form'] select[name='aspect_ratio']").val(value).closest("form").submit();
});

$(document).click(function(event) {
    if (!$(event.target).closest("#aspectRatio-filter-icon, #aspectRatio-filter-dropdown").length) {
        $("#aspectRatio-filter-dropdown").hide();
    }
});

$(document).on("click", ".delete-filter", function() {
    var name = $(this).attr("id");
    $(`form[id^='filter-form'] select[name='${name}']`).val("").closest("form").submit();
});

$(document).ready(function() {
    $('.select2').select2();
});