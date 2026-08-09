/* Playwright Practice Site - Shared JavaScript Logic */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Harmless page load console log
  console.log("Practice website loaded successfully.");

  // 2. Cookie Consent Banner logic
  initCookieBanner();

  // 3. Auth & Session Management (login.html & dashboard.html)
  initAuthLogic();

  // 4. Page Loading Spinner (~1s delay)
  initLoadingSpinner();

  // 5. Toggle Hidden Div
  initToggleDiv();

  // 6. Load More Button (~1.5s delay)
  initLoadMore();

  // 7. Toast Notification (3s auto-dismiss)
  initToastNotification();

  // 8. Custom Modal Dialog & Trap Focus
  initCustomModal();

  // 9. Native <dialog> element
  initNativeDialog();

  // 10. Accordion Component
  initAccordion();

  // 11. Tabs Component
  initTabs();

  // 12. Carousel Slider Component
  initCarousel();

  // 13. Giant Contact Form Validation & Handler
  initContactForm();

  // 14. Sortable Table
  initSortableTable();

  // 15. Paginated List
  initPaginatedList();

  // 16. File Upload Preview
  initFileUploadPreview();

  // 17. Drag and Drop Reorderable List
  initDragAndDrop();

  // 18. Back to Top Button
  initBackToTop();
});

/* Cookie Consent */
function initCookieBanner() {
  const banner = document.getElementById('cookie-banner');
  if (!banner) return;

  const isAccepted = localStorage.getItem('cookie_consent');
  if (isAccepted === 'accepted') {
    banner.classList.add('hidden');
  }

  const acceptBtn = document.getElementById('accept-cookies-btn');
  const dismissBtn = document.getElementById('dismiss-cookies-btn');

  const closeBanner = () => {
    localStorage.setItem('cookie_consent', 'accepted');
    banner.classList.add('hidden');
  };

  if (acceptBtn) acceptBtn.addEventListener('click', closeBanner);
  if (dismissBtn) dismissBtn.addEventListener('click', closeBanner);
}

/* Auth & Session Management */
function initAuthLogic() {
  // Login Form Handler
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const usernameInput = document.getElementById('login-username');
      const username = usernameInput ? usernameInput.value : 'TestUser';
      
      const fakeSession = {
        user: username || 'TestUser',
        token: 'fake-jwt-token-playwright-12345',
        timestamp: Date.now()
      };

      localStorage.setItem('auth_session', JSON.stringify(fakeSession));
      window.location.href = 'dashboard.html';
    });
  }

  // Dashboard Page Check
  const dashboardContent = document.getElementById('dashboard-content');
  const loginRequiredMsg = document.getElementById('login-required-msg');
  const userGreeting = document.getElementById('user-greeting');
  const logoutBtn = document.getElementById('logout-btn');

  if (dashboardContent && loginRequiredMsg) {
    const rawSession = localStorage.getItem('auth_session');
    if (rawSession) {
      try {
        const session = JSON.parse(rawSession);
        dashboardContent.classList.remove('hidden');
        loginRequiredMsg.classList.add('hidden');
        if (userGreeting) userGreeting.textContent = session.user;
      } catch (err) {
        dashboardContent.classList.add('hidden');
        loginRequiredMsg.classList.remove('hidden');
      }
    } else {
      dashboardContent.classList.add('hidden');
      loginRequiredMsg.classList.remove('hidden');
    }
  }

  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      localStorage.removeItem('auth_session');
      window.location.href = 'login.html';
    });
  }
}

/* Page Loading Spinner */
function initLoadingSpinner() {
  const spinner = document.getElementById('page-spinner');
  const content = document.getElementById('main-content-wrapper');

  if (spinner && content) {
    setTimeout(() => {
      spinner.classList.add('hidden');
      content.classList.remove('hidden');
    }, 1000);
  }
}

/* Toggle Hidden Div */
function initToggleDiv() {
  const toggleBtn = document.getElementById('toggle-div-btn');
  const targetDiv = document.getElementById('hidden-div-target');

  if (toggleBtn && targetDiv) {
    toggleBtn.addEventListener('click', () => {
      targetDiv.classList.toggle('hidden');
    });
  }
}

/* Load More Button (~1.5s delay) */
function initLoadMore() {
  const loadMoreBtn = document.getElementById('load-more-btn');
  const listContainer = document.getElementById('dynamic-item-list');
  let itemCounter = 3;

  if (loadMoreBtn && listContainer) {
    loadMoreBtn.addEventListener('click', () => {
      loadMoreBtn.disabled = true;
      const originalText = loadMoreBtn.textContent;
      loadMoreBtn.textContent = "Loading items...";

      setTimeout(() => {
        for (let i = 1; i <= 3; i++) {
          itemCounter++;
          const li = document.createElement('li');
          li.className = 'list-group-item';
          li.textContent = `Dynamic Item #${itemCounter} - Loaded asynchronously`;
          listContainer.appendChild(li);
        }
        loadMoreBtn.disabled = false;
        loadMoreBtn.textContent = originalText;
      }, 1500);
    });
  }
}

/* Toast Notification (3s auto-dismiss) */
function initToastNotification() {
  const triggerBtn = document.getElementById('trigger-toast-btn');
  const toastContainer = document.getElementById('toast-container');

  if (triggerBtn && toastContainer) {
    triggerBtn.addEventListener('click', () => {
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.setAttribute('role', 'alert');
      toast.setAttribute('data-testid', 'toast-alert');
      toast.innerHTML = `<span>Notification: Action performed successfully!</span>`;

      toastContainer.appendChild(toast);

      setTimeout(() => {
        toast.remove();
      }, 3000);
    });
  }
}

/* Custom Modal Dialog & Focus Trap */
function initCustomModal() {
  const openBtn = document.getElementById('open-modal-btn');
  const modalOverlay = document.getElementById('custom-modal-overlay');
  const closeBtn = document.getElementById('close-modal-btn');

  if (!modalOverlay) return;

  const openModal = () => {
    modalOverlay.classList.remove('hidden');
    modalOverlay.setAttribute('aria-hidden', 'false');
    if (closeBtn) closeBtn.focus();
  };

  const closeModal = () => {
    modalOverlay.classList.add('hidden');
    modalOverlay.setAttribute('aria-hidden', 'true');
    if (openBtn) openBtn.focus();
  };

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) closeModal();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !modalOverlay.classList.contains('hidden')) {
        closeModal();
      }
    });
  }
}

/* Native <dialog> */
function initNativeDialog() {
  const openBtn = document.getElementById('open-native-dialog-btn');
  const nativeDialog = document.getElementById('native-dialog');
  const closeBtn = document.getElementById('close-native-dialog-btn');

  if (openBtn && nativeDialog) {
    openBtn.addEventListener('click', () => {
      nativeDialog.showModal();
    });
  }

  if (closeBtn && nativeDialog) {
    closeBtn.addEventListener('click', () => {
      nativeDialog.close();
    });
  }
}

/* Accordion Component */
function initAccordion() {
  const headers = document.querySelectorAll('.accordion-header');
  headers.forEach(header => {
    header.addEventListener('click', () => {
      const body = header.nextElementSibling;
      const isOpen = body.classList.contains('open');

      // Close all accordion bodies in this accordion
      const parentAccordion = header.closest('.accordion');
      if (parentAccordion) {
        parentAccordion.querySelectorAll('.accordion-body').forEach(b => b.classList.remove('open'));
        parentAccordion.querySelectorAll('.accordion-header').forEach(h => h.setAttribute('aria-expanded', 'false'));
      }

      if (!isOpen) {
        body.classList.add('open');
        header.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* Tabs Component */
function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-button');
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetPanelId = button.getAttribute('aria-controls');
      const tabsContainer = button.closest('.tabs');

      if (tabsContainer && targetPanelId) {
        tabsContainer.querySelectorAll('.tab-button').forEach(btn => {
          btn.classList.remove('active');
          btn.setAttribute('aria-selected', 'false');
        });

        tabsContainer.querySelectorAll('.tab-panel').forEach(panel => {
          panel.classList.remove('active');
        });

        button.classList.add('active');
        button.setAttribute('aria-selected', 'true');
        const targetPanel = document.getElementById(targetPanelId);
        if (targetPanel) targetPanel.classList.add('active');
      }
    });
  });
}

/* Carousel Slider */
function initCarousel() {
  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');
  const inner = document.getElementById('carousel-inner');

  if (prevBtn && nextBtn && inner) {
    let currentIndex = 0;
    const items = inner.querySelectorAll('.carousel-item');
    const totalItems = items.length;

    const updateSlide = () => {
      inner.style.transform = `translateX(-${currentIndex * 100}%)`;
    };

    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % totalItems;
      updateSlide();
    });

    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + totalItems) % totalItems;
      updateSlide();
    });
  }
}

/* Giant Contact Form Validation & Handler */
function initContactForm() {
  const form = document.getElementById('giant-contact-form');
  if (!form) return;

  const passwordInput = document.getElementById('password-field');
  const passwordError = document.getElementById('password-error-msg');
  const successAlert = document.getElementById('contact-success-msg');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let isValid = true;

    // Custom Server-Side Style Password Length Validation (min 8 chars)
    if (passwordInput && passwordError) {
      if (passwordInput.value.length < 8) {
        passwordError.classList.remove('hidden');
        isValid = false;
      } else {
        passwordError.classList.add('hidden');
      }
    }

    if (isValid) {
      if (successAlert) {
        successAlert.classList.remove('hidden');
        successAlert.focus();
      }
    }
  });
}

/* Sortable Table */
function initSortableTable() {
  const table = document.getElementById('sortable-table');
  if (!table) return;

  const headers = table.querySelectorAll('th[data-sort]');
  headers.forEach((header, index) => {
    header.addEventListener('click', () => {
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      const isAscending = header.getAttribute('data-order') === 'asc';

      rows.sort((rowA, rowB) => {
        const cellA = rowA.children[index].textContent.trim();
        const cellB = rowB.children[index].textContent.trim();

        const numA = parseFloat(cellA.replace(/[^0-9.-]+/g, ""));
        const numB = parseFloat(cellB.replace(/[^0-9.-]+/g, ""));

        if (!isNaN(numA) && !isNaN(numB)) {
          return isAscending ? numB - numA : numA - numB;
        }

        return isAscending
          ? cellB.localeCompare(cellA)
          : cellA.localeCompare(cellB);
      });

      header.setAttribute('data-order', isAscending ? 'desc' : 'asc');
      rows.forEach(row => tbody.appendChild(row));
    });
  });
}

/* Paginated List */
function initPaginatedList() {
  const prevBtn = document.getElementById('prev-page-btn');
  const nextBtn = document.getElementById('next-page-btn');
  const pageIndicator = document.getElementById('page-indicator-text');
  const listItems = document.querySelectorAll('.paginated-item');
  const itemsPerPage = 3;

  if (listItems.length === 0 || !prevBtn || !nextBtn || !pageIndicator) return;

  let currentPage = 1;
  const totalPages = Math.ceil(listItems.length / itemsPerPage);

  const renderPage = (page) => {
    listItems.forEach((item, index) => {
      const start = (page - 1) * itemsPerPage;
      const end = page * itemsPerPage;
      if (index >= start && index < end) {
        item.classList.remove('hidden');
      } else {
        item.classList.add('hidden');
      }
    });

    pageIndicator.textContent = `Page ${page} of ${totalPages}`;
    prevBtn.disabled = page === 1;
    nextBtn.disabled = page === totalPages;
  };

  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderPage(currentPage);
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage++;
      renderPage(currentPage);
    }
  });

  renderPage(1);
}

/* File Upload Preview */
function initFileUploadPreview() {
  const fileInput = document.getElementById('file-input-single');
  const fileNamePreview = document.getElementById('selected-file-name-preview');

  if (fileInput && fileNamePreview) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        fileNamePreview.textContent = `Selected File: ${fileInput.files[0].name}`;
      } else {
        fileNamePreview.textContent = "No file selected";
      }
    });
  }
}

/* Drag and Drop Reorderable List */
function initDragAndDrop() {
  const dragList = document.getElementById('drag-drop-list');
  if (!dragList) return;

  let draggedItem = null;

  dragList.querySelectorAll('.drag-item').forEach(item => {
    item.addEventListener('dragstart', (e) => {
      draggedItem = item;
      setTimeout(() => item.classList.add('dragging'), 0);
    });

    item.addEventListener('dragend', () => {
      draggedItem.classList.remove('dragging');
      draggedItem = null;
    });

    item.addEventListener('dragover', (e) => {
      e.preventDefault();
      const afterElement = getDragAfterElement(dragList, e.clientY);
      if (afterElement == null) {
        dragList.appendChild(draggedItem);
      } else {
        dragList.insertBefore(draggedItem, afterElement);
      }
    });
  });
}

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.drag-item:not(.dragging)')];

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

/* Back to Top Button */
function initBackToTop() {
  const backToTopBtn = document.getElementById('back-to-top-btn');
  if (!backToTopBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 200) {
      backToTopBtn.style.display = 'block';
    } else {
      backToTopBtn.style.display = 'none';
    }
  });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}
