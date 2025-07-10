document.addEventListener('DOMContentLoaded', function () {
  const filterBtn = document.querySelector('.btn-primary-dark');
  const clearBtn = document.querySelector('.btn-secondary-light');
  const monthInput = document.getElementById('monthFilter');

  filterBtn?.addEventListener('click', () => {
    const month = monthInput.value;
    if (month) {
      window.location.href = `?month=${month}`;
    }
  });

  clearBtn?.addEventListener('click', () => {
    window.location.href = window.location.pathname;
  });
});
