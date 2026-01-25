import { createListSectionItem, resetForm } from "./form.js";
import { createLoader } from "./script.js";

(function () {
  document.addEventListener("show.bs.modal", (event) => {
    let label = event.target.getAttribute("aria-labelledby");
    if (!label?.search(/^Add/)) {
      Array.from(
        event.target.querySelectorAll(
          "form div.input-group.focused.is-focused",
        ),
      ).forEach((input) => {
        input?.classList.remove("focused");
        input?.classList.remove("is-focused");
      });
    }

    Array.from(event.target.querySelectorAll("ul li[data-uid]")).forEach(
      (element) => {
        element?.remove();
      },
    );
  });
  document.addEventListener("show.bs.modal", (event) => {
    const form = event.target.querySelector("form[data-get]");

    if (form) {
      form?.reset();

      Array.from(form.querySelectorAll("input")).forEach((element) => {
        let groupElement = element.closest(".input-group");

        if (groupElement) {
          groupElement.classList.value = "input-group input-group-outline";
        }
      });

      const get = form.dataset.get;
      const id =
        event.relatedTarget.dataset.id ||
        event.relatedTarget?.closest("[data-id]")?.dataset.id;

      const url = get.replace(String.fromCharCode(64), id);

      fetch(url, {
        method: "get",
      })
        .then((response) => response.json())
        .then((data) => {
          let readonly = data?.readonly || new Array();

          let names = ["input", "textarea", "select"];

          Array.from(
            form.querySelectorAll(names.join(String.fromCharCode(44))),
          ).forEach((input) => {
            let val = data[input.id];

            input.disabled = false;
            if (Array.from(readonly).includes(input.id)) {
              input.disabled = true;
            }

            switch (input.type) {
              case "checkbox":
                input.checked = val ? true : false;

                break;

              case "file":
                let dropZone = input.closest("div.drop-zone");

                if (dropZone) {
                  let ulElement = dropZone.querySelector(".list-section ul");

                  if (ulElement) {
                    ulElement.innerHTML = "";

                    if (data.files)
                      for (const f of data.files) {
                        if (f.file_for == input.id || input.id == "files") {
                          let selector = "li[data-uid='%s']";
                          if (
                            !ulElement.querySelector(
                              selector.replace("%s", f.link),
                            )
                          ) {
                            let item = createListSectionItem(
                              f.extension,
                              f.human_size,
                              true,
                              f.file_url,
                              f.id,
                            );
                            ulElement.append(item);
                          }
                        }

                        if (!input.multiple) break;
                      }
                  } else {
                    if (input.multiple) {
                    } else {
                      // Avatar
                      let fileOutput =
                        input.parentElement.querySelector(".output");

                      if (fileOutput) fileOutput.src = val;
                    }
                  }
                }
                break;

              case "select-one":
                const divElement = document.createElement("div");
                divElement.innerHTML = val;

                const v = divElement.querySelector(".value")?.innerText;

                if (v) input.value = v;

                break;

              default:
                if (val != undefined) {
                  let multiValueInput = input.closest("div.multi-value-input");

                  if (multiValueInput) {
                    multiValueInput.classList.remove("readonly");
                    if (Array.from(readonly).includes(input.id)) {
                      multiValueInput.classList.add("readonly");
                    }

                    const valuesElement =
                      multiValueInput.querySelector("div.values");

                    Array.from(val).forEach((v) => {
                      const spanElement = document.createElement("span");
                      spanElement.classList.value =
                        "badge badge-sm bg-gradient-secondary mx-2 my-2";
                      spanElement.innerHTML = v;
                      spanElement.dataset.role = "value";

                      valuesElement.append(spanElement);
                    });
                  } else {
                    input.value = data[input.id];

                    let inputGroup = input.closest("div.input-group");
                    if (inputGroup) inputGroup.classList.add("is-filled");
                  }
                }

                break;
            }
          });
        });
    }
  });

  document.addEventListener("hidden.bs.modal", (event) => {
    const form = event.target.querySelector("form");

    if (form) resetForm(form);
  });
}).call();

(function () {
  document.addEventListener("show.bs.modal", (event) => {
    let modalDialog = event.target.querySelector(".modal-dialog");

    if (event.relatedTarget.getAttribute("aria-label") !== "View Modal") return;

    let loaderElement = createLoader();

    modalDialog.append(loaderElement);

    setInterval(() => {
      let modalBody = modalDialog.querySelector(".modal-body");

      if (modalBody.innerHTML) {
        loaderElement.classList.add("fade");
        setTimeout(() => {
          loaderElement.remove();
        }, 50);
      }
    }, 1000);
  });
  document.addEventListener("hidden.bs.modal", (event) => {
    let b = event.target.closest("#ViewModal")?.querySelector(".modal-body");
    if (b) b.innerHTML = "";
  });
}).call();
