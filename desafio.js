const tasklist = document.getElementById("taskList");
const taskInput = document.getElementById("taskInput");
const taskCategory = document.getElementById("taskCategory"); 

function addTask() {
    const taskText = taskInput.value.trim();
    const categoryText = taskCategory.value; 

     const tasksExistentes = document.querySelectorAll("#taskList li span");


    let Duplicado = false;
    tasksExistentes.forEach(task => {

        if (task.textContent.trim().toLowerCase() === taskText.toLowerCase()) {
            Duplicado = true;
        }
    });


    if (Duplicado) {
        alert("Este produto já está na lista!");
        taskInput.value = "";
        taskCategory.value = "";
        return; 
    }

   
    if (taskText !== "" && categoryText !== "") { 
        const maxText = taskText.substring(0, 35);
        const li = document.createElement("li");
        
        li.innerHTML = `
            <span>${maxText}</span>
            <span class="category">${categoryText}</span> 
            <button class="editButton" onClick="editTask(this)">Editar</button>
            <button class="deleteButton" onClick="deleteTask(this)">Remover</button>
        `;
        tasklist.appendChild(li);
        taskInput.value = "";
        taskCategory.value = ""; 
    }
}

function editTask(button) {
    const li = button.parentElement;
    const span = li.querySelector('span');  
    const oldTaskText = span.textContent.trim(); // Guarda o texto antigo para usar na validação
    
    const newTaskText = prompt('Edite a tarefa:', oldTaskText);
    
    // Se o usuário clicar em "Cancelar" ou não digitar nada, a função para.
    if (newTaskText === null || newTaskText.trim() === '') {
        return;
    }

    // --- NOVA VALIDAÇÃO: VERIFICAR DUPLICATAS ---
    const allTasks = document.querySelectorAll("#taskList li");
    
    for (const taskLi of allTasks) {
        // Encontra o span dentro do item da lista atual do loop
        const taskSpan = taskLi.querySelector('span');

        // Se o item que está sendo verificado NÃO é o item que estamos editando...
        if (taskLi !== li) {
            // E se o texto do novo nome for igual a um dos nomes existentes...
            if (taskSpan.textContent.trim().toLowerCase() === newTaskText.trim().toLowerCase()) {
                alert("Já existe uma tarefa com este nome na lista!");
                return; // Impede a edição
            }
        }
    }

}

function deleteTask(button) {
    const confirmDelete = confirm('Tem certeza que deseja remover esta tarefa?');
    if (!confirmDelete) {
        return;
    }
    const li = button.parentElement;
    tasklist.removeChild(li);

}











