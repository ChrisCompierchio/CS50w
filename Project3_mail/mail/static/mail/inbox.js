document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#send').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-page').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-page').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;


  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(message => {
      const element = document.createElement('div');

      if (message.read == true){
        element.className = "single-read";
      } else {
        element.className = "single";
      }
      element.innerHTML = `
        <br/>
        <h4> From: ${message.sender}</h4>
        <br/>
        <h5> To: ${message.recipients}</h4>
        <h6> At: ${message.timestamp} </h6>
        <br/>
        <h5> Subject: ${message.subject} </h5>
        <br/>
        <p> ${message.body} </p>
      `;
      element.addEventListener('click', function() {
        view_email(message.id)
      });
      document.querySelector('#emails-view').append(element);
    })


  });

}

function send_email() {

  event.preventDefault();

  let r = document.querySelector('#compose-recipients').value;
  let s = document.querySelector('#compose-subject').value;
  let b = document.querySelector('#compose-body').value;


  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: r,
        subject: s,
        body: b
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
  });
}

function view_email(email_id){

  document.querySelector('#email-page').innerHTML = "";

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-page').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(message => {

    const element = document.createElement('div');
    element.innerHTML = `
      <br/>
      <br/>
      <h4> To: ${message.recipients} </h4>
      <br/>
      <h4> From: ${message.sender} </h4>
      <br/>
      <h6> At: ${message.timestamp} </h6>
      <br/>
      <h5> Subject: ${message.subject} </h5>
      <br/>
      <p>${message.body}</p>
      <br/>
      <br/>
    `;

      if (message.sender != document.querySelector('#user_email').innerHTML){
        let archive_btn = document.createElement('button');
        archive_btn.innerHTML = message.archived ? "Unarchive" : "Archive";

        archive_btn.addEventListener('click', function(){
          if (message.archived){
            unarchive(message.id);
          }else{
            archive(message.id);
          }
        });


        document.querySelector('#email-page').append(archive_btn);
      }

      fetch(`/emails/${message.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })

      let reply = document.createElement('button');
      reply.innerHTML = "Reply";

      reply.addEventListener('click', function(){
        reply_view(message);
      });

      document.querySelector('#email-page').append(element);
      document.querySelector('#email-page').append(reply);


  });

}

function archive(email_id){

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(message => {
    fetch(`/emails/${message.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  })
  .then(() => [load_mailbox('archive')]);
}

function unarchive(email_id){

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(message => {
    fetch(`/emails/${message.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  })
  .then(() => [load_mailbox('inbox')]);
}

function reply_view(response){

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-page').style.display = 'none';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-recipients').value = response.sender;

  if(response.subject.charAt(0) === 'R' && response.subject.charAt(1) === 'e' && response.subject.charAt(2) === ':'){
    document.querySelector('#compose-subject').value = response.subject;
  } else{
    document.querySelector('#compose-subject').value = `Re: ${response.subject}`;
  }

  document.querySelector('#compose-body').placeholder = `On ${response.timestamp} ${response.sender} wrote: ${response.body}`;
}
