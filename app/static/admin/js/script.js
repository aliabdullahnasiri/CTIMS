function activeTab(presentation) {
  const aElement = presentation.querySelector("[aria-selected=true]");

  if (aElement) {
    const tab = document.querySelector(
      "[data-tab-id='%s']".replace("%s", aElement.dataset.bsTarget),
    );

    if (tab) {
      const tabContainer = tab.closest("[role=tab-container]");

      tabContainer?.querySelectorAll("[role=tab]").forEach((element) => {
        element.classList.add("d-none");
      });

      tab.classList.remove("d-none");
      tab.classList.add("show");
    }
  }
}

export function transformMovingTab(movingTab, presentation) {
  const presentationRect = presentation.getBoundingClientRect();

  movingTab.style.width = `${presentationRect.width}px`;
  movingTab.style.height = `${presentationRect.height}px`;
  movingTab.style.left = `${presentation.offsetLeft}px`;

  if (presentation) activeTab(presentation);
}

export function transformAllMovingTab() {
  for (const tabElement of document.querySelectorAll("[role=tablist]")) {
    let presentation = tabElement.querySelector(
      "[role=presentation]:has(a[aria-selected=true])",
    );
    let movingTab = tabElement.querySelector(".moving-tab");

    if (presentation && movingTab) {
      transformMovingTab(movingTab, presentation);
      activeTab(presentation);
    }
  }
}

export function createMovingTab(presentation) {
  const divElement = document.createElement("div");

  divElement.style.width = presentation.offsetWidth + "px";
  divElement.style.height = presentation.offsetHeight + "px";
  divElement.style.transition = "0.5s";

  divElement.classList.value =
    "moving-tab position-absolute nav-link bg-gradient-dark";

  return divElement;
}

export function initAllMovingTabs() {
  for (const tabElement of document.querySelectorAll("[role=tablist]")) {
    let presentation = tabElement.querySelector("[role=presentation]");

    if (presentation) {
      let movingTab = createMovingTab(presentation);
      tabElement.append(movingTab);
      transformMovingTab(movingTab, presentation);
      activeTab(presentation);
    }
  }
}

export function createLoader() {
  let divElement = document.createElement("div");

  divElement.classList.value =
    "bg-gradient-dark position-absolute w-100 h-100 z-index-10000 rounded-2";

  divElement.dataset.bsRole = "loader";

  return divElement;
}

(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const loaderElement = document.querySelector("div[data-bs-role=loader]");

    setTimeout(() => {
      loaderElement.classList.add("fade");
      setTimeout(() => {
        loaderElement.remove();
      }, 500);
    }, 2000);
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

  window.addEventListener("resize", () => {
    transformAllMovingTab();
  });

  document.addEventListener("resize", () => {
    transformAllMovingTab();
  });
}).call();

(function () {
  if (getComputedStyle(document.body).direction === "rtl") {
    const $inputs = $("input.form-control[type=date]");

    $inputs.each(function () {
      const $input = $(this);

      $input.persianDatepicker({
        months: [
          "حمل",
          "ثور",
          "جوزا",
          "سرطان",
          "اسد",
          "سنبله",
          "میزان",
          "عقرب",
          "قوس",
          "جدی",
          "دلو",
          "حوت",
        ],
        dowTitle: [
          "شنبه",
          "یکشنبه",
          "دوشنبه",
          "سه شنبه",
          "چهارشنبه",
          "پنج شنبه",
          "جمعه",
        ],
        shortDowTitle: ["ش", "ی", "د", "س", "چ", "پ", "ج"],
        showGregorianDate: false,
        persianNumbers: true,
        formatDate: "YYYY/MM/DD",
        selectedBefore: false,
        selectedDate: null,
        startDate: null,
        endDate: null,
        prevArrow: "◄",
        nextArrow: "►",
        theme: "default",
        alwaysShow: false,
        selectableYears: null,
        selectableMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        cellWidth: 25,
        cellHeight: 20,
        fontSize: 13,
        isRTL: true,
        calendarPosition: {
          x: 0,
          y: 0,
        },
        onShow: function () {},
        onHide: function () {},
        onSelect: function () {
          const d = new Date($input.context.dataset.gdate);
          $input.context.value =
            d.getFullYear() +
            "-" +
            String(d.getMonth() + 1).padStart(2, "0") +
            "-" +
            String(d.getDate()).padStart(2, "0");
        },
        onRender: function () {},
      });
    });
  }
}).call(this);

(function () {
  const sideNavElement = document.querySelector("#sidenav-collapse-main");
  const ps = new PerfectScrollbar(sideNavElement, {
    suppressScrollX: true,
  });
}).call(this);

(function () {
  $(document).ready(function () {
    $("select").selectpicker();
  });
}).call(this);
