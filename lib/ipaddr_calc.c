#include <stdio.h>
#include <stdint.h>
#include <memory.h>
#include <stdlib.h>
#include <string.h>

void countToArr(uint8_t* out, uint32_t const* count)
{
    uint8_t result[4];
    memset(result,0,sizeof(result));

    uint32_t tmp = *count / 256; 
    result[3] = *count % 256;

    if ( tmp >= 256 ) {
        result[1] = tmp / 256;
        result[2] = tmp % 256;
    } else {
        result[2] = tmp;
    }

    memcpy(out,result,sizeof(result));
    out = result;
}

uint32_t sumIP(uint8_t const* first, uint8_t const* second)
{
    uint32_t first_32 = ( (uint8_t)( first[0] ) << 24 ) |
                        ( (uint8_t)( first[1] ) << 16 ) |
                        ( (uint8_t)( first[2] ) << 8  ) |
                          (uint8_t)( first[3] );

    uint32_t second_32 = ( (uint8_t)( second[0] ) << 24 ) |
                         ( (uint8_t)( second[1] ) << 16 ) |
                         ( (uint8_t)( second[2] ) << 8  ) |
                           (uint8_t)( second[3] );

    uint32_t sum_32 = first_32+second_32-1;

    return sum_32;
}

void parseIP( uint8_t* ip, char const* ip_str)
{
    sscanf( ip_str, "%hhu.%hhu.%hhu.%hhu", &ip[0], &ip[1], &ip[2], &ip[3] );
}

char* maxIP( char const* ip, uint32_t count )
{
    uint8_t count_arr[4];
    uint8_t start_ip[4];
    uint8_t sum[4];
    uint32_t sum_32;

    parseIP( start_ip, ip );
    countToArr( count_arr, &count );

    sum_32 = sumIP( start_ip, count_arr );

    memset(sum, 0, sizeof(sum));
    sum[0] = (uint8_t)( sum_32 >> 24 );
    sum[1] = (uint8_t)( sum_32 >> 16 );
    sum[2] = (uint8_t)( sum_32 >> 8  );
    sum[3] = (uint8_t)( sum_32 );

    char* max_ip = (char*)malloc( sizeof(char) * (20) );

    int n = 0;
    for ( int i = 0; i != sizeof( sum ); ++i) {
        n += sprintf( &max_ip[n], "%u", sum[i] );
        n += sprintf( &max_ip[n], "%s", "." );
    }
    memset( &max_ip[n-1], '\0', 1 );

    return max_ip;
}
