


########################################################################
class MDC

    #----------------------------------------------------------------------
    constructor: () ->

        #Drawer
        drawerEl = document.querySelector('.mdc-temporary-drawer');
        MDCTemporaryDrawer = mdc.drawer.MDCTemporaryDrawer;
        @drawer = new MDCTemporaryDrawer(drawerEl);

        #slider = new mdc.slider.MDCSlider(document.querySelector('.mdc-slider'));
        #slider.listen('MDCSlider:change', () => console.log(`Value changed to ${slider.value}`));


$(document).ready ->

#csrftoken for AJAX
#----------------------------------------------------------------------
    #Ajax setup for use CSRF tokens
    csrftoken = $.cookie("csrftoken")
    csrfSafeMethod = (method) -> (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
    $.ajaxSetup
        beforeSend: (xhr, settings) ->
            if not csrfSafeMethod(settings.type) and not @crossDomain
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
    window.csrftoken = csrftoken
#----------------------------------------------------------------------



    MDC = new MDC();

    $(".mdc-toolbar .mdc-toolbar__menu-icon").first().on "click", () ->
        MDC.drawer.open = true;

    $(".mdc-fab--exited").removeClass("mdc-fab--exited")

    for element in $(".mdc-icon-toggle")
        mdc.iconToggle.MDCIconToggle.attachTo(element)

    for element in $(".mdc-slider")
        mdc.slider.MDCSlider.attachTo(element)

    for element in $(".mdc-textfield")
        mdc.textfield.MDCTextfield.attachTo(element)






    MDL_Layout = new Hammer($("body")[0])
    MDL_Layout.get("pan").set
        velocity: 100
        pointers: 1
        threshold: 2
        direction: Hammer.DIRECTION_HORIZONTAL
    MDL_Layout.on "panright", (event) ->
        if event
            if event.center.x > 30 or event.center.x is 0
                return
        MDC.drawer.open = true;




