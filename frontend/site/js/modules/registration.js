import { apiRequest, USER_EMAIL_KEY } from './api.js';

function setMessage(element, message, isError = false) {
  if (!element) return;
  element.textContent = message || '';
  element.style.color = isError ? '#ff7a7a' : '#8ef0b3';
}

function initTabs() {
  const tabRegister = document.getElementById('tabRegister');
  const tabLogin = document.getElementById('tabLogin');
  const panelRegister = document.getElementById('panelRegister');
  const panelLogin = document.getElementById('panelLogin');

  if (!tabRegister || !tabLogin || !panelRegister || !panelLogin) {
    return { setActiveTab: () => {} };
  }

  function setActiveTab(mode) {
    const loginActive = mode === 'login';

    tabLogin.classList.toggle('auth-tab--active', loginActive);
    panelLogin.classList.toggle('auth-panel--active', loginActive);
    tabRegister.classList.toggle('auth-tab--active', !loginActive);
    panelRegister.classList.toggle('auth-panel--active', !loginActive);

    tabLogin.setAttribute('aria-selected', loginActive ? 'true' : 'false');
    tabRegister.setAttribute('aria-selected', loginActive ? 'false' : 'true');
  }

  tabRegister.addEventListener('click', () => setActiveTab('register'));
  tabLogin.addEventListener('click', () => setActiveTab('login'));

  const params = new URLSearchParams(window.location.search);
  setActiveTab(params.get('tab') === 'login' ? 'login' : 'register');

  return { setActiveTab };
}

function initRegisterForm({ setActiveTab }) {
  const form = document.getElementById('registrationForm');
  const messageEl = document.getElementById('registrationMessage');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setMessage(messageEl, '');

    const formData = new FormData(form);
    const name = String(formData.get('name') || '').trim();
    const email = String(formData.get('email') || '').trim().toLowerCase();
    const password = String(formData.get('password') || '');
    const passwordConfirm = String(formData.get('passwordConfirm') || '');

    if (!name) return setMessage(messageEl, 'Please enter your name.', true);
    if (!email) return setMessage(messageEl, 'Please enter your email.', true);
    if (password.length < 6) {
      return setMessage(messageEl, 'Password must be at least 6 characters.', true);
    }
    if (password !== passwordConfirm) {
      return setMessage(messageEl, 'Passwords do not match.', true);
    }

    try {
      const data = await apiRequest('/users/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password }),
      });

      if (data?.status !== 'success') {
        throw new Error(data?.message || 'Registration failed.');
      }

      localStorage.setItem(USER_EMAIL_KEY, email);
      localStorage.setItem(
        'anaida_registration',
        JSON.stringify({ name, email, registeredAt: new Date().toISOString() }),
      );

      setMessage(messageEl, data.message || 'Registration successful.');

      setTimeout(() => {
        setActiveTab('login');
        const loginEmail = document.getElementById('loginEmail');
        if (loginEmail) loginEmail.value = email;
      }, 500);
    } catch (error) {
      setMessage(messageEl, error.message || 'Registration failed.', true);
    }
  });
}

function initLoginForm() {
  const form = document.getElementById('loginForm');
  const messageEl = document.getElementById('loginMessage');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setMessage(messageEl, '');

    const formData = new FormData(form);
    const email = String(formData.get('email') || '').trim().toLowerCase();
    const password = String(formData.get('password') || '');

    if (!email || !password) {
      return setMessage(messageEl, 'Please enter email and password.', true);
    }

    try {
      const data = await apiRequest('/users/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      if (data?.status !== 'success') {
        throw new Error(data?.message || 'Login failed.');
      }

      localStorage.setItem(USER_EMAIL_KEY, email);
      setMessage(messageEl, data.message || 'Login successful.');

      setTimeout(() => {
        window.location.href = 'index.html';
      }, 400);
    } catch (error) {
      setMessage(messageEl, error.message || 'Login failed.', true);
    }
  });
}

function initGoogleFallback() {
  window.handleCredentialResponse = async () => {
    const target = document.getElementById('loginMessage') || document.getElementById('registrationMessage');
    setMessage(
      target,
      'Google sign-in is not connected on backend yet. Use email/password for now.',
      true,
    );
  };
}

export function initRegistration() {
  const tabs = initTabs();
  initRegisterForm(tabs);
  initLoginForm();
  initGoogleFallback();
}
