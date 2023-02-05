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

      const finalTime = `${strPadLeft(minutes, '0', 2)} : ${strPadLeft(seconds, '0', 2)}`;
      $flash.textContent = `You can try again in ${finalTime}.`

      total_seconds -= 1;

      if (total_seconds < 0) {
        $flash.textContent = `You can try resend now.`
        clearInterval(interval)
      }
    }, 1000)
  });
});
