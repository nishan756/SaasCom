const chips = document.querySelectorAll('.chip');

chips.forEach(chip => {
  chip.addEventListener('click', function(e) {
    e.preventDefault();

    chips.forEach(c => c.classList.remove('active'));
    this.classList.add('active');

    // auto scroll into view (nice UX)
    this.scrollIntoView({behavior: 'smooth', inline: 'center'});
  });
});