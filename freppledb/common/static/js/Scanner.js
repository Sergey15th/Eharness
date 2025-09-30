      class KeyBuffer {
        constructor() {
	  console.log('Scanner driver init ...');
          this.buffer = '';
          this.timer = null;
          this.delay = 50; // Задержка в миллисекундах
          this.backendUrl = '/api/barcode-scanned/'; // URL вашего бэкенда

          // Инициализация прослушивателя событий
          this.initEventListener();
          }
          initEventListener() {
	    console.log('Add event listener ...');
            document.addEventListener('keydown', (event) => {              
              // Игнорируем специальные клавиши
              if (event.ctrlKey || event.altKey || event.metaKey || event.key==='Shift') return;
              // Очищаем предыдущий таймер
              if (this.timer) {
                clearTimeout(this.timer);
              }
              // Добавляем клавишу в буфер
              this.buffer += event.key;
              // Устанавливаем новый таймер
              this.timer = setTimeout(() => {
                //!this.buffer.length
                if (this.buffer.length < 5) {
                  this.buffer = '';
                  return;
                  }
                  else {
                    this.sendToBackend();
                  };
              }, this.delay);
            });
          }
        async sendToBackend() {
	  console.log('Send to backend ...');
          // Сохраняем текущий буфер и очищаем
          const textToSend = this.buffer;
    console.log('Text to send ...' + textToSend);
          this.buffer = '';
          // const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];

          fetch(this.backendUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'X-CSRFToken': getCSRFToken(),  // 👈 Передаём CSRF-токен
            },
            body: `barcode=${encodeURIComponent(textToSend)}`
            })
            .then(response => response.json())
            .then(data => {
              if (data.status === 'success') {
                  console.log(`Успешно: ${data.status}`);
                  // alert(`Успешный вход как: ${data.username}`);
                  if (data.action==='workstation_set') {document.cookie = 'workstation_id='+ data.data + '; max-age=3600; path=/; secure'}; // secure - только HTTPS}
                  if (data.action==='item_solderinglist_open' ||
                      data.action==='item_operationmaterial_open' ||
                      data.action==='item_cutlist_open'
                    ) {
                      document.cookie = 'item_id='+ data.data + '; max-age=3600; path=/; secure'
                    }; // secure - только HTTPS}
                  console.log(`Успешно: ${data.data}`);
                  if (data.reload)
                    {
                      location.reload();// Обновляем страницу
                    }
                  else if (data.redirect) {window.location.href = data.redirect_url;}  // или полный URL}
                } else {
                    console.log('Ошибка: ' + (data.message || 'Неизвестная ошибка'));
                    // alert('Ошибка: ' + (data.message || 'Неизвестная ошибка'));
                    }
              });
          function getCSRFToken() {
          return document.cookie.match(/csrftoken=([^;]+)/)[1];
          }        
        }}

      // Инициализация при загрузке страницы
      document.addEventListener('DOMContentLoaded', () => {
        console.log('Document.addEventListener ...');
        new KeyBuffer();
        });

