document.addEventListener('DOMContentLoaded', function() {
    const generateButton = document.getElementById('generate-user');
    const mainContent = document.getElementById('main-content');
    const addUserForm = document.getElementById('add-user-form');

    generateButton.addEventListener('click', function() {
        // Générer un nom d'utilisateur et un mot de passe aléatoires
        const generatedUsername = generateRandomString(8);
        const generatedPassword = generateRandomString(10);

        document.getElementById('username').value = generatedUsername;
        document.getElementById('password').value = generatedPassword;
    });

    // Fonction pour générer une chaîne aléatoire de longueur donnée
    function generateRandomString(length) {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@/è-ér&)àç_(#~{|][';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result;
    }
});
