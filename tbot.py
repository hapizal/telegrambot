import psutil
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_API_TOKEN' with your actual bot token
API_TOKEN = 'YOUR_API_TOKEN'


# Get local server system health
def get_system_health():
    host = subprocess.check_output(['hostname']).decode('UTF-8').strip()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    health_report = (
        f"Hostname: {host}\n"
        f"---------------------------\n"
        f"CPU Usage: {cpu_usage}%\n"
        f"Memory Usage: {memory.percent}%\n"
        f"Disk Usage: {disk.percent}%"
    )

    return health_report

# Execute any message on telegram chat as bash command
def execute_bash_command(command):
    """
    Executes a bash command and returns the output.

    Parameters:
    command (str): The bash command to execute.

    Returns:
    str: The output of the command.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Command failed with error: {stderr.decode('utf-8')}"

    return stdout.decode('utf-8')

# Read any new feed on the file
def readx():
    try:
        with open('file.txt', 'r') as file:
            content = file.readlines()
            if content:
                return content[0]  # Return the first line for simplicity
            else:
                return "File is empty"
    except FileNotFoundError:
        return "File not found"


# Function to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(get_system_health())


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = 'ps -ef | grep bot'
    output = execute_bash_command(command)
    await update.message.reply_text(output)


async def read(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    content = readx()
    await update.message.reply_text(content)


# Function to execute any bash command from message
async def execute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text  # Get the command from the message text
    output = execute_bash_command(command)
    await update.message.reply_text(output)


# Function to handle errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


def main() -> None:
    # Create the Application
    application = ApplicationBuilder().token(API_TOKEN).build()

    # Add command handler for the /check command
    application.add_handler(CommandHandler("check244", start))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("read", read))

    # Add message handler to execute all messages as commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, execute))

    # Log all errors
    application.add_error_handler(error)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    application.run_polling()


if __name__ == '__main__':
    main()

