$(document).ready(function () {
  $(".collapsible").collapsible({ accordion: !0 }),
    $(".carousel.carousel-slider").carousel({ fullWidth: !0 }),
    $(".carousel").carousel(),
    $(".dropdown-trigger").dropdown({
      alignment: "right",
      constrainWidth: !1,
      coverTrigger: !1,
      closeOnClick: !1,
      onOpenEnd: function (t) {
        console.log(t.M_Dropdown);
        var e = $(this).find(".tabs"),
          i = t.M_Dropdown;
        if (e.length) {
          var n = M.Tabs.getInstance(e);
          n.updateTabIndicator(),
            (n.options.onShow = function () {
              setTimeout(function () {
                i.recalculateDimensions(), n.updateTabIndicator();
              }, 0);
            });
        }
      },
    }),
    $(".slider").slider(),
    $(".parallax").parallax(),
    $(".modal").modal(),
    $(".scrollspy").scrollSpy(),
    $(".sidenav").sidenav({ edge: "left" }),
    $("#sidenav-right").sidenav({ edge: "right" }),
    $(".datepicker").datepicker({ selectYears: 20 }),
    $("select").not(".disabled").formSelect(),
    $("input.autocomplete").autocomplete({
      data: {
        Apple: null,
        Microsoft: null,
        Google: "http://placehold.it/250x250",
      },
    }),
    $(".tabs").tabs(),
    $(".chips").chips(),
    $(".chips-initial").chips({
      readOnly: !0,
      data: [{ tag: "Apple" }, { tag: "Microsoft" }, { tag: "Google" }],
    }),
    $(".chips-placeholder").chips({
      placeholder: "Enter a tag",
      secondaryPlaceholder: "+Tag",
    }),
    $(".chips-autocomplete").chips({
      autocompleteOptions: {
        data: { Apple: null, Microsoft: null, Google: null },
      },
    });
});
