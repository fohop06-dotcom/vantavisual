document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem('jwtToken');
  if (!token) {
    window.location.href = '/signin';
    return;
  }

  try {
    const res = await fetch(`${window.location.origin}/api/v1/account/details`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();

    if (data.success && data.data) {
      const user = data.data;
      document.querySelectorAll('.user-name, .header-name').forEach(el => el.textContent = user.login);
      document.querySelectorAll('.id').forEach(el => el.textContent = user.id);
      document.querySelectorAll('.email').forEach(el => el.textContent = user.email);

      if (user.created_at) {
        const date = new Date(user.created_at);
        document.querySelector('.creation').textContent = date.toLocaleDateString('ru-RU');
      }
    }
  } catch (e) {
    console.error('Failed to load profile:', e);
  }

  document.getElementById('logout-btn')?.addEventListener('click', () => {
    localStorage.removeItem('jwtToken');
    window.location.href = '/signin';
  });

  document.querySelectorAll('.popup-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.popup-overlay').style.display = 'none';
    });
  });

  document.getElementById('enter-key-btn')?.addEventListener('click', () => {
    document.getElementById('key-popup-overlay').style.display = 'flex';
  });

  document.getElementById('twofa-btn')?.addEventListener('click', () => {
    document.getElementById('twofa-popup-overlay').style.display = 'flex';
  });
});
