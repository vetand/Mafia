from fpdf import FPDF
import playerDatabase
import pika, sys, os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_FOLDER = 'Images/'
REPORT_FOLDER = 'Reports/'

def generate_report(player_id):
    try:
        print("Generate report of player {}".format(player_id))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 18)

        player_info = playerDatabase.get_player(player_id)
        stats_info = playerDatabase.get_player_stats(player_id)

        try:
            for extension in ALLOWED_EXTENSIONS:
                try:
                    pdf.image(name = "{}{}.{}".format(IMAGE_FOLDER,
                                                    player_id,
                                                    extension), w = 40, h = 40)
                except Exception as e:
                    pass
        except Exception as e:
            print('Database error: ', e)

        pdf.cell(80, 10, 'Nickname: {}'.format(player_info['name']), ln=1)
        pdf.cell(80, 10, 'Gender: {}'.format(player_info['gender']), ln=1)
        pdf.cell(80, 10, 'E-mail: {}'.format(player_info['email']), ln=1)
        pdf.cell(80, 10, 'Games complited: {}'.format(stats_info['games_complited']), ln=1)
        pdf.cell(80, 10, 'Total victories: {}'.format(stats_info['victories']), ln=1)
        pdf.cell(80, 10, 'Total defeats: {}'.format(stats_info['defeats']), ln=1)
        pdf.cell(80, 10, 'Total time in game: {} seconds'.format(stats_info['overall_time_played']), ln=1)

        pdf.output('{}{}.pdf'.format(REPORT_FOLDER, player_id)).encode('latin-1')
    except Exception as e:
        return None

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='report')

    def callback(ch, method, properties, body):
        generate_report(int(body))

    channel.basic_consume(queue='report', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)