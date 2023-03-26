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
    });
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

  (document.querySelectorAll(".business") || []).forEach(($business) => {
    $business.addEventListener("click", (e) => {
      window.location.href = `/business/view/${$business.dataset.id}`;
    })
  });

  const getBusinessItems = async (businessId) => {
    let response = await fetch(`/business/items/${businessId}`);
    return await response.json();
  }

  document.querySelector(".ticket-item-form #is_business_item")?.addEventListener("change", (e) => {
    $form = e.target.closest('form');
    
    if (e.target.checked) {
      $nameSelectInput = document.querySelector('select');
      $nameSelectInput.textContent = '';

      getBusinessItems($form.dataset.businessId).then(businessItems => {
        for (let businessItem of businessItems) {
          let $optionElement = document.createElement("option");
          $optionElement.innerText = businessItem;
          $optionElement.setAttribute("value", businessItem);
          $nameSelectInput.appendChild($optionElement);
        }
      });

      $nameInput = document.getElementById('name').closest('.field').setAttribute('hidden', true);
      $nameInput = document.getElementById('name').setAttribute('disabled', true);
      $nameSelectInput.closest('.field').removeAttribute('hidden');
      $nameSelectInput.removeAttribute('disabled');
    }
    else {
      $nameSelectInput = document.querySelector('select').closest('.field').setAttribute('hidden', true);
      $nameSelectInput = document.querySelector('select').setAttribute('disabled', true);
      $nameInput = document.querySelector('#name').closest('.field').removeAttribute('hidden');
      $nameInput = document.querySelector('#name').removeAttribute('disabled');
    }
  }); 

  document.querySelector(".ticket-item-form select")?.closest('.field').setAttribute('hidden', true);
  document.querySelector(".ticket-item-form select")?.setAttribute('disabled', true);

  document.querySelector('.ticket-item-form')?.addEventListener('submit', (e) => {
    e.preventDefault()
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);

    let name;
    if (formProps.is_business_item == 'y') {
      name = formProps.business_items;
    }
    else {
      name = formProps.name;
    }

    let requirement = formProps.requirement;


    if (!name || !requirement) {
      alert('Please enter all the details.');
      return;
    }
    
    $ticketItems = document.querySelector('.ticket-items');

    $div = document.createElement('div');
    $div.classList.add('ticket-item', 'level', 'm-1', 'p-2');

    $nameParagraph = document.createElement('p');
    $nameParagraph.classList.add('ticket-item-name');
    $nameParagraph.textContent = name;

    $requirementParagraph = document.createElement('p');
    $requirementParagraph.classList.add('ticket-item-requirement');
    $requirementParagraph.textContent = requirement;

    $deleteIconContainer = document.createElement('div');
    $deleteIconContainer.classList.add('ticket-item-delete');
    $deleteIcon = document.createElement('i');
    $deleteIcon.classList.add('fas', 'fa-trash', 'is-clickable');
    $deleteIconContainer.appendChild($deleteIcon);
    $deleteIconContainer.addEventListener('click', (e) => {
      if (confirm('Are you sure want to delete this?')) {
        e.target.closest('.ticket-item').remove();
      }
    });

    $div.appendChild($nameParagraph);
    $div.appendChild($requirementParagraph);
    $div.appendChild($deleteIconContainer);

    $ticketItems.appendChild($div);
  });

  document.querySelector('.create-ticket')?.addEventListener('click', async (e) => {
    $ticketItems = e.target.parentElement.parentElement.querySelectorAll('.ticket-item');

    let ticketItems = [];
    for (let $ticketItem of $ticketItems) {
      let name = $ticketItem.querySelector('.ticket-item-name').textContent;
      let requirement = $ticketItem.querySelector('.ticket-item-requirement').textContent;
      ticketItems.push({name: name, requirement: requirement})
    }

    $form = document.querySelector('form');
    response = await fetch(`/business/ticket?id=${$form.dataset.businessId}`, 
                      { 
                        method: 'POST',
                        headers: {
                          'Accept': 'application/json',
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(ticketItems)
                      }
                    );
    await response.json().then(() => {
        window.location.href = '/customer/tickets';
    });
  });

  (document.querySelectorAll(".ticket") || []).forEach(($ticket) => {
    $ticket.addEventListener("click", (e) => {
      window.location.href = `/customer/tickets/${$ticket.dataset.id}`;
    })
  });

  (document.querySelectorAll(".business-ticket") || []).forEach(($ticket) => {
    $ticket.addEventListener("click", (e) => {
      window.location.href = `/business/tickets/${$ticket.dataset.id}`;
    })
  });

  document.querySelector(".ticket-comment-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    const comment = formProps.comment.trim();

    if (!comment) {
      alert('Please enter a comment...')
    }

    await fetch(`/business/tickets/${e.target.dataset.ticketId}/comment`,
    { 
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'comment': comment})
    })
      .then((data) => data.json())
      .then((data) => console.log(data));

    e.target.reset();

    window.location.reload();
  });
});
