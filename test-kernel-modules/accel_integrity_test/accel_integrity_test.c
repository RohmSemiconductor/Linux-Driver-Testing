#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <getopt.h>

struct arguments  {
	char *samplerate;
	char *scale;
};

void* thread_samplerate(void* vargs)
{
	char command[100];
	int clen;
	FILE *p;
	struct arguments *arguments;

	arguments = (struct arguments*)vargs;

	printf("thread_samplerate: %s\n", arguments->samplerate);

	strcat(command, "echo ");
	strcat(command, arguments->samplerate);
	strcat(command, " > /sys/devices/platform/generic_accel_test/iio_channels/sampling_frequency");

	printf("samplerate command: %s\n", command);

	p = popen(command, "r");

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

	arguments = (struct arguments*)vargs;

	printf("thread scale: %s\n", arguments->scale);

	strcat(command, "echo ");
	strcat(command, arguments->scale);
	strcat(command, " > /sys/devices/platform/generic_accel_test/iio_channels/scale");

	p = popen(command, "r");

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

	printf("Before Thread\n");

	pthread_create(&thread_id1, NULL, thread_samplerate, (void*)arguments);
	pthread_create(&thread_id2, NULL, thread_scale, (void*)arguments);

	pthread_join(thread_id1, NULL);
	pthread_join(thread_id2, NULL);
	printf("After Thread\n");

	return 0;
}
