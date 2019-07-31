
var notesNav;

if (document.location.pathname.search("blog") >= 0) {
    notesNav = document.getElementsByClassName('mainNavLiBlogs')[0];
}
if (document.location.pathname.search("note") >= 0) {
    notesNav = document.getElementsByClassName('mainNavLiNotes')[0];
}
notesNav.className = notesNav.className + " active";

var sideNavCat = document.getElementsByClassName("navNoteCat"+activeCat)[0];
sideNavCat.className = sideNavCat.className + " active";
