export function transformMovingTab(movingTab, presentation) {
  movingTab.style.transform = "translate3d(%spx, 0px, 0px)".replace(
    "%s",
    presentation?.offsetLeft,
  );
}

export function createMovingTab(presentation) {
  const divElement = document.createElement("div");

  divElement.style.width = presentation.offsetWidth + "px";
  divElement.style.height = presentation.offsetHeight + "px";
  divElement.style.transition = "0.5s";
  divElement.style.transform = "translate3d(%spx, 0px, 0px)".replace(
    "%s",
    presentation.offsetLeft,
  );

  divElement.classList.value =
    "moving-tab position-absolute nav-link bg-gradient-dark";

  return divElement;
}

export function initAllMovingTabs() {
  for (const tabElement of document.querySelectorAll("[role=tablist]")) {
    let presentation = tabElement.querySelector("[role=presentation]");

    if (presentation) tabElement.append(createMovingTab(presentation));
  }
}

(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const loaderElement = document.querySelector("div[data-bs=loader]");

    setTimeout(() => {
      loaderElement.classList.add("fade");
      setTimeout(() => {
        loaderElement.remove();
      }, 500);
    }, 500);
  });

  document.addEventListener("click", (event) => {
    const tabListElement = event.target.closest("[role=tablist]");

    if (tabListElement) {
      const presentation = event.target.closest("[role=presentation]");
      const movingTab = tabListElement.querySelector("div.moving-tab");

      if (!movingTab) {
        tabListElement.append(createMovingTab(presentation));
      } else {
        transformMovingTab(movingTab, presentation);
      }
    }
  });
}).call();
