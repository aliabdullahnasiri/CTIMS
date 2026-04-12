(function () {
  const asideElement = document.querySelector("aside");
  const fixedPluginElement = document.querySelector(".fixed-plugin");
  const badgeColorsElement = fixedPluginElement.querySelector(".badge-colors");
  const sideNavTypeElement = fixedPluginElement.querySelector(".sidenav-type");
  const darkVersionElement = fixedPluginElement.querySelector("#dark-version");

  const badgeColor = localStorage.getItem("side-bar-color");
  const sideNavType = localStorage.getItem("side-nav-type");
  const darkVersion = localStorage.getItem("dark-version");

  let spanElement = badgeColorsElement.querySelector(
    "span[data-color='{}']".replace("{}", badgeColor ? badgeColor : "dark"),
  );
  let sidebarTypeElement = sideNavType
    ? fixedPluginElement.querySelector(
        "button[data-class='{}']".replace("{}", sideNavType),
      )
    : "bg-gradient-dark";

  badgeColorsElement.addEventListener("click", function (event) {
    if (event.target.tagName == "SPAN")
      localStorage.setItem("side-bar-color", event.target.dataset.color);
  });

  sideNavTypeElement.addEventListener("click", function (event) {
    if (event.target.tagName == "BUTTON") {
      localStorage.setItem("side-nav-type", event.target.dataset.class);
    }
  });

  darkVersionElement.addEventListener("change", function (event) {
    localStorage.setItem("dark-version", event.target.checked);
    if (sidebarTypeElement) sidebarType(sidebarTypeElement);
  });

  document.addEventListener("DOMContentLoaded", () => {
    Array.from(asideElement.querySelectorAll("a")).forEach((aElement) => {
      const url = new URL(aElement.href);
      if (url.pathname == location.pathname) {
        aElement.classList.remove("text-dark");
        aElement.classList.add("active");
      } else aElement.classList.remove("active");
    });

    try {
      if (spanElement) sidebarColor(spanElement);
    } catch (error) {
      console.error(error);
    }

    try {
      if (sidebarTypeElement) sidebarType(sidebarTypeElement);
    } catch (error) {}

    try {
      if (darkVersion == "true") {
        darkVersionElement.checked = darkVersion;

        if (darkVersionElement) darkMode(darkVersionElement);
        if (sidebarTypeElement) sidebarType(sidebarTypeElement);
      }
    } catch (error) {
      console.error(error);
    }
  });
}).call();
