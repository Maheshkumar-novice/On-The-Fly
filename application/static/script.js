document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );

  (document.querySelectorAll(".is-timer .flash-message") || []).forEach(($flash) => {
    let total_seconds = Number($flash.textContent.trim());
    let minutes;
    let seconds;
    $flash.textContent = `You can try again in few minutes.`

    function strPadLeft(string, pad, length) {
      return (new Array(length + 1).join(pad) + string).slice(-length);
    }

    let interval = setInterval(() => {
      minutes = Math.floor(total_seconds / 60);
      seconds = Math.floor(total_seconds % 60);

      const finalTime = `${strPadLeft(minutes, "0", 2)} : ${strPadLeft(seconds, "0", 2)}`;
      $flash.textContent = `You can try again in ${finalTime}.`

      total_seconds -= 1;

      if (total_seconds < 0) {
        $flash.textContent = `You can try resend now.`
        clearInterval(interval)
      }
    }, 1000)
  });

  (document.querySelectorAll("input[type='password']") || []).forEach(($input) => {
    const passwordRegExp = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,50}$/;
    $input.addEventListener("input", () => {
      $passwordHelpText = $input.nextElementSibling
      if (!passwordRegExp.test($input.value)) {
        $passwordHelpText.classList.remove("is-hidden");
      }
      else {
        $passwordHelpText.classList.add("is-hidden");
      }
    })
  });
  
  const getBusinessSubTypes = async (businessType) => {
    let response = await fetch(`/business/subtypes?type=${businessType}`);
    return await response.json();
  }
  
  const $businessSubTypeSelectElement = document.querySelector("select#business_subtype");
  document.querySelector("select#business_type")?.addEventListener("change", (e) => {
    $businessSubTypeSelectElement.innerHTML = '';

    getBusinessSubTypes(e.target.value).then(businessSubTypes => {
      for (let businessSubType of businessSubTypes) {
        let $optionElement = document.createElement("option");
        $optionElement.innerText = businessSubType;
        $optionElement.setAttribute("value", businessSubType);
        $businessSubTypeSelectElement.appendChild($optionElement);
      }
    })
  });

  (document.querySelectorAll(".navbar-burger") || []).forEach(($burger) => {
    $burger.addEventListener("click", () => {
      const target = $burger.dataset.target;
      const $target = document.getElementById(target);

      $burger.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    })
  });

  (document.querySelectorAll(".business-item") || []).forEach(($businessItem) => {
    $businessItem.addEventListener("click", (e) => {
      window.location.href = `/business/edit_item?id=${$businessItem.dataset.id}`;
    })
  });

  (document.querySelectorAll(".business-item-delete") || []).forEach(($businessItemDelete) => {
    $businessItemDelete.addEventListener("click", async (e) => {
      e.stopPropagation();
      $deletionTarget = e.target.closest('.business-item');
      
      const confirmation = confirm('Are you sure want to delete this item?');

      if (confirmation) {
        response = await fetch(`/business/delete_item?id=${$deletionTarget.dataset.id}`, { method: 'DELETE' });
        await response.json().then(() => {
          window.location.href = '/business/items';
        });
      }
    })
  });
});