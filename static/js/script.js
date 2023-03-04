const alertEL = document.querySelector(".alert");

if (alertEL) {
  setTimeout(() => {
    alertEL.remove()
  }, 3000);
}
