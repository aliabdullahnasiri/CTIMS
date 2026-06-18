export function uploadFile(
  file,
  on_progress,
  on_abort,
  on_upload_load,
  on_load,
  on_loadstart,
  on_loadend,
  user_uid,
  file_for,
) {
  let http = new XMLHttpRequest();
  let data = new FormData();

  data.append("file", file);
  if (user_uid != undefined) data.append("user_uid", user_uid);
  if (file_for != undefined) {
    data.append("file_for", file_for);
  }

  http.upload.addEventListener("progress", on_progress);
  http.upload.addEventListener("abort", on_abort);
  http.upload.addEventListener("load", on_upload_load);
  http.upload.addEventListener("loadstart", on_loadstart);
  http.upload.addEventListener("loadend", on_loadend);

  http.addEventListener("load", on_load);

  http.open("POST", "/api/upload", true);
  http.send(data);

  return http;
}

export function resetForm(formElement) {
  formElement.reset();

  // Reset Multi-Value Input
  for (const input of formElement.querySelectorAll("div.multi-value-input")) {
    for (const val of input?.querySelectorAll(
      "div.values span[data-role=value]",
    ))
      val.remove();
  }
}

async function submitForm(formElement) {
  const formData = new FormData(formElement);

  const files = {};

  let inputElement, dropZone, ulElement, liElements, liElement, outputElement;
  for (const [key, value] of formData.entries()) {
    if (typeof value == "object") {
      inputElement = formElement.querySelector(
        String.fromCharCode(35).concat(key),
      );
      dropZone = inputElement.closest("div.drop-zone");

      if (inputElement && inputElement.type == "file") {
        if (dropZone) {
          outputElement = dropZone.querySelector(".output");

          if (outputElement) {
            if (!(key in files)) {
              if (outputElement.tagName == "IMG") {
                files[key] = +outputElement.dataset.uid;
              }
            }
          } else {
            if (!(key in files)) files[key] = new Array();
            ulElement = dropZone.querySelector(".list-section ul");

            if (ulElement) {
              liElements = ulElement.querySelectorAll("li");

              for (liElement of liElements) {
                if (!files[key].includes(liElement.dataset.uid))
                  files[key].push(+liElement.dataset.uid);
              }
            }
          }
        }
      }
    }
  }

  for (const [key, val] of formData.entries()) {
    if (typeof val == "object") {
      formData.delete(key);
    }
  }

  formData.append("files", JSON.stringify(files));

  formElement.querySelectorAll("div.multi-value-input").forEach((element) => {
    const valuesElement = element.querySelector("div.values");
    const spanElements = valuesElement.querySelectorAll("span");
    const inputElement = element.querySelector("input");

    formData.set(
      inputElement.name,
      JSON.stringify(
        Array.from(spanElements).map((element) => element.innerHTML),
      ),
    );
  });

  let form = formElement;

  let eventInitDict = { bubbles: true };
  try {
    const response = await fetch(form.action, {
      method: form.method,
      body: formData,
    });

    const data = await response.json();

    eventInitDict.detail = data;

    // Clear previous errors
    form.querySelectorAll(".errors").forEach((el) => el.remove());
    form
      .querySelectorAll(".is-invalid")
      .forEach((el) => el.classList.remove("is-invalid"));

    if (data.errors) {
      Object.entries(data.errors).forEach(([key, messages]) => {
        const input = form.querySelector(`#${key}`);
        if (!input) return;

        if (input.dataset.onError == "alert") {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: Array.from(messages).join("\n"),
          });
        } else {
          const parent = input.parentElement;
          parent.classList.add("is-invalid");

          const errorDiv = document.createElement("div");
          errorDiv.classList.add("errors");
          errorDiv.classList.add("px-2");

          messages.forEach((msg) => {
            const span = document.createElement("span");
            span.className = "text-danger small";
            span.textContent = msg;
            errorDiv.appendChild(span);
          });

          parent.parentElement.appendChild(errorDiv);
        }
      });
    } else {
      Swal.fire({
        title: data.title,
        text: data.message,
        icon: data.category,
      }).then(() => {
        if (data?.redirect) {
          window.location.replace(data.redirect);
        }
      });
    }
  } catch (err) {
    console.log(err);
  }

  form.dispatchEvent(new CustomEvent("afterSubmit", eventInitDict));
}

export function humanizeFileSize(size, si = false) {
  const POWER = !si ? 1000 : 1024;

  if (size < 1000) {
    return size + "B";
  } else if (size > 1000 && size < 1000000) {
    return Math.round(size / POWER) + "K";
  } else if (size > 1000000 && size < 1000000000) {
    return Math.round(size / POWER ** 2) + "MB";
  } else if (size > 1000000000 && size < 1000000000000) {
    return Math.round(size / POWER ** 3) + "Gib";
  }

  return size;
}

export function shortFileType(type) {
  if (type.length <= 4) {
    return type;
  } else {
    if (type.includes("ISO")) {
      return "ISO";
    } else if (type.includes("ICO")) {
      return "ICO";
    }
  }

  return type.slice(0, 5).concat("...");
}

export function validateFileType(file) {}

export function createListSectionItem(extension, size, uploaded, link, uid) {
  let liElement = document.createElement("li");
  let divHeaderElement = document.createElement("div");
  let divFooterElement = document.createElement("div");
  let divBodyElement = document.createElement("div");
  let divContentElement = document.createElement("div");
  let deleteButtonElement = document.createElement("button");
  let deleteIconElement = document.createElement("i");
  let typeSpanElement = document.createElement("span");
  let sizeSpanElement = document.createElement("span");

  if (uploaded && link) {
    liElement.dataset.url = link;
    liElement.dataset.uid = uid;
  }

  liElement.classList.value =
    "card w-20 height-100 p-2 mx-2 my-2 position-relative cursor-pointer";
  divHeaderElement.classList.value =
    "header position-absolute end-0 mt-n3 me-n2";
  divBodyElement.classList.value = "body h-100 d-grid align-items-end";
  divFooterElement.classList.value = "footer mt-2";
  deleteButtonElement.classList.value =
    "btn btn-danger btn-sm rounded-circle p-0 m-0 delete-item";
  deleteIconElement.classList.value = "material-symbols-rounded fs-5";
  divContentElement.classList.value = "d-grid";

  typeSpanElement.style.lineHeight = "20px";
  sizeSpanElement.classList.value = "text-xs";

  deleteButtonElement.dataset.role = uploaded ? "delete-file" : "abort";

  deleteIconElement.innerHTML = uploaded ? "delete" : "close";

  typeSpanElement.innerText = extension;
  sizeSpanElement.innerText = size;

  deleteButtonElement.type = "button";

  deleteButtonElement.append(deleteIconElement);
  divHeaderElement.append(deleteButtonElement);
  divContentElement.append(typeSpanElement, sizeSpanElement);
  divBodyElement.append(divContentElement);

  liElement.append(divHeaderElement, divBodyElement);

  if (!uploaded) {
    let progressBarElement = createProgressBar("0", "0", "100");

    divFooterElement.append(progressBarElement);
    liElement.append(divFooterElement);
  }

  return liElement;
}

function u(file, ulElement, formElement, submitElement) {
  const [type, size] = [
    shortFileType(file.type.split(String.fromCharCode(47)).pop().toUpperCase()),
    humanizeFileSize(file.size),
  ];

  let item = createListSectionItem(type, size);
  let progressBar = item.querySelector("div.progress-bar");
  let abortButton = item.querySelector("div.header button");
  let uidInput = formElement.querySelector("input[type=hidden][name=user_uid]");

  ulElement.append(item);

  let http = uploadFile(
    file,
    (e) => {
      progressBar.style.width = String((e.loaded / e.total) * 100).concat(
        String.fromCharCode(37),
      );
    },
    () => {
      item.remove();
    },
    () => {
      item.querySelector("div.header button i").innerHTML = "delete";
      item.querySelector("div.header button").dataset.role = "delete-file";

      progressBar.closest("div.footer")?.remove();
    },

    (e) => {
      try {
        let data = JSON.parse(e.target.response);

        for (let d of data) {
          if (d?.file?.id) item.dataset.uid = d.file.id;

          break;
        }
      } catch (err) {
        console.log(err);
      }
    },
    () => {
      if (formElement) {
        submitElement.disabled = true;
      }
    },
    () => {
      if (formElement) {
        submitElement.disabled = false;
      }
    },
    uidInput?.value,
  );

  abortButton.addEventListener("click", () => {
    http.abort();
  });
}

export function createProgressBar(now_value, min_value, max_value) {
  let divElement = document.createElement("div");
  let progressBarElement = document.createElement("div");

  divElement.classList.value = "progress";
  progressBarElement.classList.value =
    "bg-gradient-success progress-bar progress-bar-animated progress-bar-striped";

  progressBarElement.setAttribute("role", "progressbar");
  progressBarElement.setAttribute("aria-valuenow", now_value ? now_value : "0");
  progressBarElement.setAttribute("aria-valuemin", min_value ? min_value : "0");
  progressBarElement.setAttribute(
    "aria-valuemax",
    max_value ? max_value : "100",
  );

  progressBarElement.style.width = (max_value / 100) * now_value + "%";

  divElement.append(progressBarElement);

  return divElement;
}

export function upload(files, dropZone) {
  if (dropZone) {
    let formElement = dropZone.closest("form");
    let submitElement = formElement?.querySelector("input[type=submit]");
    let inputElement = dropZone.querySelector("input[type=file]");

    if (inputElement) {
      if (inputElement.multiple) {
        let ulElement = dropZone.querySelector(".list-section ul");

        if (ulElement) {
          for (const file of files) {
            u(file, ulElement, formElement, submitElement);
          }
        }
      } else {
        for (const file of files) {
          let ulElement = dropZone.querySelector(".list-section ul");

          if (ulElement) {
            ulElement.innerHTML = String();

            u(file, ulElement, formElement, submitElement);
          } else if (file?.type.includes("image")) {
            let outputElement = dropZone.querySelector("img.output");
            let uidInput = formElement.querySelector(
              "input[type=hidden][name=uid], input[type=hidden][name=user_uid]",
            );

            uploadFile(
              file,
              () => {}, // on progress
              () => {}, // on abort
              () => {}, // on upload load
              (e) => {
                try {
                  let data = JSON.parse(e.target.response);

                  if (outputElement) {
                    for (const d of data) {
                      if (d?.file?.file_url) {
                        outputElement.dataset.url = d.file.file_url;
                        outputElement.dataset.uid = d.file.id;
                        outputElement.src = d.file.file_url;
                      }

                      break;
                    }
                  }
                } catch (err) {
                  console.log(err);
                }
              }, // on load
              undefined,
              undefined,
              uidInput?.value,
              "AVATAR",
            );
          }

          break;
        }
      }

      const dataTransfer = new DataTransfer();

      if (inputElement.multiple) {
        for (const file of inputElement.files) {
          dataTransfer.items.add(file);
        }

        for (const file of files) {
          dataTransfer.items.add(file);
        }
      } else {
        for (const file of files) {
          dataTransfer.items.add(file);

          break;
        }
      }

      inputElement.files = dataTransfer.files;
    }
  }
}

(function () {
  document.addEventListener("dragover", (event) => {
    const dropZoneElement = event.target.closest("div.drop-zone");
    if (dropZoneElement) {
      event.preventDefault();

      dropZoneElement.classList.add("drag-over-effect");
    }
  });

  document.addEventListener("dragleave", (event) => {
    if (event.target.classList.contains("drop-zone")) {
      event.preventDefault();

      event.target.classList.remove("drag-over-effect");
    }
  });

  document.addEventListener("drop", (event) => {
    let dropZone = event.target.closest("div.drop-zone");

    if (dropZone) {
      event.preventDefault();

      event.target.classList.remove("drag-over-effect");

      upload(event.dataTransfer.files, dropZone);
    }
  });

  document.addEventListener("submit", (event) => {
    event.preventDefault();

    switch (event.target.tagName) {
      case "FORM":
        submitForm(event.target);

        break;
    }
  });

  document.addEventListener("click", (event) => {
    if (event.target.tagName == "IMG") {
      if (event.target.classList.contains("output")) {
        let fileOutput = event.target;
        let dropZone = event.target.closest("div.drop-zone");
        let fileInput = dropZone.querySelector("input[type=file]");

        if (fileInput && fileOutput) fileInput.click();
      }
    } else if (
      event.target.tagName == "SPAN" &&
      event.target.closest("div.multi-value-input") &&
      event.target.dataset.role == "value"
    ) {
      if (
        !event.target
          .closest("div.multi-value-input")
          .classList.contains("readonly")
      )
        event.target.remove();
    } else if (event.target.closest("button[data-role=delete-file]")) {
      let liElement = event.target.closest("li[data-url],li[data-uid]");

      if (liElement) liElement.remove();
    } else if (
      event.target.tagName == "STRONG" &&
      event.target.classList.contains("open-default-file-input-modal")
    ) {
      let formElement = event.target.closest("form");
      let inputElement = formElement.querySelector(
        "input#".concat(event.target.dataset.id),
      );

      inputElement?.click();
    } else {
      let closest = event.target.closest("li.file-card[data-url]");
      if (closest) {
        window.open(
          window.location.protocol +
            "//" +
            window.location.host +
            closest.dataset.url,
          "blank",
        );
      }
    }
  });

  document.addEventListener("change", (event) => {
    if (event.target.type == "file") {
      const dropZone = event.target.closest("div.drop-zone");
      if (dropZone) upload(event.target.files, dropZone);
    }
  });

  document.addEventListener("keydown", (event) => {
    {
      let multiValueInput = event.target.closest("div.multi-value-input");

      if (multiValueInput && event.key == "Enter") {
        event.preventDefault();

        let valuesElement = multiValueInput.querySelector("div.values");
        let spanElement = document.createElement("span");

        spanElement.classList.value =
          "badge badge-sm bg-gradient-secondary mx-2 my-1 cursor-pointer tt-none";
        spanElement.innerHTML = event.target.value;
        spanElement.dataset.role = "value";

        valuesElement.append(spanElement);

        event.target.value = "";
      }
    }
  });

  document.querySelectorAll("form").forEach((formElement) => {
    formElement.noValidate = true;
  });
})();

(function () {
  document.body.addEventListener(
    "focusin",
    (event) => {
      const target = event.target;

      if (Array("INPUT", "TEXTAREA").includes(target.tagName)) {
        const inputGroup = target.closest(".input-group");

        Array.from(document.querySelectorAll("div.suggestions-list")).forEach(
          (element) => {
            if (inputGroup && inputGroup.contains(element)) {
              return; // Skip this one
            }

            element.classList.add("d-none");
          },
        );
      }
    },
    true,
  );

  document.body.addEventListener(
    "click",
    (event) => {
      const target = event.target;

      if (target.closest("div.suggestions-list,.input-group")) return;

      Array.from(document.querySelectorAll("div.suggestions-list")).forEach(
        (element) => {
          element.classList.add("d-none");
        },
      );
    },
    true,
  );

  const handler = function (event) {
    const target = event.target;

    if (
      target.tagName !== "INPUT" ||
      target.dataset.autoComplete !== "true" ||
      (target.value.length < 3 && event.type !== "focus" && event.keyCode !== 8)
    )
      return;

    const parentElement = target.parentElement;

    let suggestionsListDivElement = parentElement.querySelector(
      "div.suggestions-list",
    );

    if (!suggestionsListDivElement) {
      suggestionsListDivElement = document.createElement("div");
      suggestionsListDivElement.classList.value =
        "m-0 mt-2 position-absolute rounded-2 suggestions-list top-100 w-100 z-index-2 p-0 pb-2";

      parentElement.append(suggestionsListDivElement);
    }

    suggestionsListDivElement.classList.remove("d-none");

    let url = target.dataset.fetchApi;

    if (url) {
      const query = target.value;

      let params = new URLSearchParams();

      params.set("query", query);
      params.set("model-name", target.dataset.modelName);
      params.set("search-col", target.dataset.searchCol);
      params.set("select-val", target.dataset.selectVal);
      params.set("template", target.dataset.template);

      url = url.concat(String.fromCharCode(63)).concat(params.toString());

      fetch(url)
        .then((response) => response.text())
        .then((data) => {
          suggestionsListDivElement.innerHTML = data;
        });
    }
  };

  document.body.addEventListener("focus", handler, true);
  document.body.addEventListener("keyup", handler, true);
  document.body.addEventListener(
    "click",
    (event) => {
      const target = event.target;
      const suggestionsListDivElement = target.closest("div.suggestions-list");
      const itemElement = target.closest(".item");

      if (!suggestionsListDivElement || !itemElement) return;

      suggestionsListDivElement.classList.add("d-none");

      const inputGroup = target.closest("div.input-group");
      const inputElement = inputGroup.querySelector(
        "input[data-auto-complete=true]",
      );
      const selectVal = inputElement.dataset.selectVal;

      let val = itemElement.getAttribute(
        "data".concat(String.fromCharCode(45)).concat(selectVal),
      );

      const valsElement =
        inputGroup?.parentElement?.querySelector("div.values");

      inputElement.value = "";

      if (valsElement && !valsElement.innerHTML.includes(val)) {
        let spanElement = document.createElement("span");
        spanElement.classList.value =
          "badge badge-sm bg-gradient-secondary mx-2 my-1 cursor-pointer tt-none";
        spanElement.dataset.role = "value";
        spanElement.innerHTML = val;

        valsElement.append(spanElement);
      }

      if (!valsElement) {
        inputGroup.classList.add("is-filled");
        inputElement.value = val;
      }
    },
    true,
  );
}).call(this);

(function () {
  document.body.addEventListener("click", (event) => {
    const liElement = event.target.closest("li[data-url][data-uid]");
    const deleteFileButton = event.target.closest(
      "button[data-role='delete-file']",
    );

    if (liElement && deleteFileButton) {
      let id = liElement.dataset.uid;

      fetch("/api/delete/file/".concat(id))
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        });
    }
  });
}).call(this);

(function () {
  $(document).on(
    "changed.bs.select",
    "select",
    async function (e, clickedIndex, isSelected, previousValue) {
      const parentSelect = this;

      const dependents = document.querySelectorAll(
        `select[data-depends-on="${parentSelect.id}"]`,
      );

      for (const childSelect of dependents) {
        const valCol = childSelect.dataset.optionValue;
        const textCol = childSelect.dataset.optionText;
        const api = childSelect.dataset.fetchApi;

        const $child = $(childSelect);

        $child.selectpicker("destroy");

        // clear old options
        childSelect.innerHTML = "";

        try {
          const response = await fetch(
            `${api}?${valCol}=${encodeURIComponent($(parentSelect).val())}`,
          );

          const items = await response.json();

          for (const item of items) {
            childSelect.add(new Option(item[textCol], item[valCol]));
          }

          childSelect.selectedIndex = -1;

          $child.selectpicker();

          // optional: trigger next level dependency
          $child.trigger("changed.bs.select");
        } catch (err) {
          console.error("Error loading dependent select:", err);
        }
      }
    },
  );
}).call(this);

(function () {
  function fun(select) {
    select.querySelectorAll("option").forEach((option) => {
      for (let group of document?.querySelectorAll(
        `[data-group-id='${option.value}']`,
      )) {
        group = group?.closest(".row,.group");
        if (select.value !== option.value) group.classList.add("d-none");
        else group.classList.remove("d-none");
      }
    });
  }

  document.querySelectorAll("[data-group-switcher=true]").forEach((select) => {
    fun(select);
  });

  document.addEventListener("change", (event) => {
    if (!event.target.matches("select") && !event.target.dataset.groupSwitcher)
      return;

    fun(event.target);
  });
}).call(this);

(function () {
  //
  const input = document.getElementById("electronic_tazkira_number");

  input.addEventListener("input", (e) => {
    let value = e.target.value.replace(/\D/g, "");

    if (value.length > 13) {
      value = value.slice(0, 13);
    }

    if (value.length > 8) {
      value = `${value.slice(0, 4)}-${value.slice(4, 8)}-${value.slice(8)}`;
    } else if (value.length > 4) {
      value = `${value.slice(0, 4)}-${value.slice(4)}`;
    }

    e.target.value = value;
  });
}).call(this);
