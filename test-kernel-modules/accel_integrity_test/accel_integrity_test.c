#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <getopt.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>

struct arguments  {
	char *samplerate;
	char *scale;
};

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;


void* trigger_thread(void* vargs)
{
	pthread_mutex_lock(&mutex);
	pthread_cond_wait(&cond, &mutex);
	pthread_mutex_unlock(&mutex);
	printf("trigger_thread: released mutex\n");
	return NULL;
}


void* thread_samplerate(void* vargs)
{
	char command[100];
	int clen;
	FILE *p;
	struct arguments *arguments;

	struct timeval tt;
	arguments = (struct arguments*)vargs;


	printf("thread_samplerate: %s\n", arguments->samplerate);
	printf("thread_samplerate: waiting for release\n");

	strcat(command, "echo ");
	strcat(command, arguments->samplerate);
	strcat(command, " > /sys/devices/platform/generic_accel_test/iio_channels/sampling_frequency");


	pthread_mutex_lock(&mutex);
	pthread_cond_wait(&cond, &mutex);
	pthread_mutex_unlock(&mutex);

	gettimeofday(&tt, NULL);
	printf("Started at: %ld\n", tt.tv_usec);

	p = popen(command, "r");
	printf("samplerate command: %s\n", command);

	if (p == NULL)
		printf("Unable to run: sample rate command\n");

	pclose(p);

	return NULL;
}

void* thread_scale(void *vargs)
{
	char command[100];
	FILE *p;
	int ch;
	struct arguments *arguments;

	struct timeval tt;
	arguments = (struct arguments*)vargs;


	printf("thread scale: %s\n", arguments->scale);
	printf("thread_scale: waiting for release\n");

	strcat(command, "echo ");
	strcat(command, arguments->scale);
	strcat(command, " > /sys/devices/platform/generic_accel_test/iio_channels/scale");

	pthread_mutex_lock(&mutex);
	pthread_cond_wait(&cond, &mutex);
	pthread_mutex_unlock(&mutex);

	gettimeofday(&tt, NULL);
	printf("Started at: %ld\n", tt.tv_usec);

	p = popen(command, "r");
	printf("scale command: %s\n", command);

	if (p == NULL)
		printf("Unable to run: scale command\n");

	pclose(p);

	return NULL;
}

int main(int argc, char* argv[])
{
	int c;
	pthread_t thread_id1;
	pthread_t thread_id2;
	pthread_t thread_id3;
	struct arguments *arguments;

	arguments = malloc(sizeof(struct arguments));

	while ((c = getopt(argc, argv, "-s:-r:")) != -1){
		switch (c) {
			case 'r':
				arguments->samplerate = strdup(optarg);
				break;
			case 's':
				arguments->scale = strdup(optarg);
				break;
		}
	}

	printf("Before threads\n");

//	pthread_create(&thread_id1, NULL, trigger_thread, NULL);
	pthread_create(&thread_id2, NULL, thread_samplerate, (void*)arguments);
	pthread_create(&thread_id3, NULL, thread_scale, (void*)arguments);
	sleep(2);
	pthread_cond_broadcast(&cond);
//	pthread_join(thread_id1, NULL);
	pthread_join(thread_id2, NULL);
	pthread_join(thread_id3, NULL);
	printf("After threads\n");

	return 0;
}
