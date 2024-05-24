document.addEventListener("DOMContentLoaded", function() {
  const menuToggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("menu");
  let startX;

  menuToggle.addEventListener("click", () => {
    toggleMenu();
  });

  menu.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
  });

  menu.addEventListener("touchmove", (e) => {
    const currentX = e.touches[0].clientX;
    const diffX = startX - currentX;

    if (Math.abs(diffX) > 50) {
      if (diffX > 0) {
        menu.classList.add("hidden");
      }
    }
  });
});

function toggleMenu() {
  const menu = document.getElementById("menu");
  menu.classList.toggle("hidden");
}
