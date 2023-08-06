/*
 * Unknown 0x74 (shell item) values functions
 *
 * Copyright (C) 2010-2017, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <byte_stream.h>
#include <memory.h>
#include <types.h>

#include "libfwsi_debug.h"
#include "libfwsi_file_attributes.h"
#include "libfwsi_libcerror.h"
#include "libfwsi_libcnotify.h"
#include "libfwsi_libfdatetime.h"
#include "libfwsi_libfguid.h"
#include "libfwsi_shell_folder_identifier.h"
#include "libfwsi_unknown_0x74_values.h"

/* Creates unknown 0x74 values
 * Make sure the value unknown_0x74_values is referencing, is set to NULL
 * Returns 1 if successful or -1 on error
 */
int libfwsi_unknown_0x74_values_initialize(
     libfwsi_unknown_0x74_values_t **unknown_0x74_values,
     libcerror_error_t **error )
{
	static char *function = "libfwsi_unknown_0x74_values_initialize";

	if( unknown_0x74_values == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid unknown 0x74 values.",
		 function );

		return( -1 );
	}
	if( *unknown_0x74_values != NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_ALREADY_SET,
		 "%s: invalid unknown 0x74 values value already set.",
		 function );

		return( -1 );
	}
	*unknown_0x74_values = memory_allocate_structure(
	                        libfwsi_unknown_0x74_values_t );

	if( *unknown_0x74_values == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_INSUFFICIENT,
		 "%s: unable to create unknown 0x74 values.",
		 function );

		goto on_error;
	}
	if( memory_set(
	     *unknown_0x74_values,
	     0,
	     sizeof( libfwsi_unknown_0x74_values_t ) ) == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_MEMORY,
		 LIBCERROR_MEMORY_ERROR_SET_FAILED,
		 "%s: unable to clear unknown 0x74 values.",
		 function );

		goto on_error;
	}
	return( 1 );

on_error:
	if( *unknown_0x74_values != NULL )
	{
		memory_free(
		 *unknown_0x74_values );

		*unknown_0x74_values = NULL;
	}
	return( -1 );
}

/* Frees unknown 0x74 values
 * Returns 1 if successful or -1 on error
 */
int libfwsi_unknown_0x74_values_free(
     libfwsi_unknown_0x74_values_t **unknown_0x74_values,
     libcerror_error_t **error )
{
	static char *function = "libfwsi_unknown_0x74_values_free";

	if( unknown_0x74_values == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid unknown 0x74 values.",
		 function );

		return( -1 );
	}
	if( *unknown_0x74_values != NULL )
	{
		memory_free(
		 *unknown_0x74_values );

		*unknown_0x74_values = NULL;
	}
	return( 1 );
}

/* Reads the unknown 0x74 values
 * Returns the number of bytes read if successful or -1 on error
 */
ssize_t libfwsi_unknown_0x74_values_read(
         libfwsi_unknown_0x74_values_t *unknown_0x74_values,
         const uint8_t *shell_item_data,
         size_t shell_item_data_size,
         int ascii_codepage,
         libcerror_error_t **error )
{
	static char *function         = "libfwsi_unknown_0x74_values_read";
	size_t shell_item_data_offset = 0;
	size_t string_alignment_size  = 0;
	size_t string_size            = 0;
	uint16_t data_size            = 0;

#if defined( HAVE_DEBUG_OUTPUT )
	uint32_t value_32bit          = 0;
	uint16_t value_16bit          = 0;
#endif

	if( unknown_0x74_values == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid unknown 0x74 values.",
		 function );

		return( -1 );
	}
	if( shell_item_data == NULL )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_INVALID_VALUE,
		 "%s: invalid shell item data.",
		 function );

		return( -1 );
	}
	if( shell_item_data_size > (size_t) SSIZE_MAX )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_ARGUMENTS,
		 LIBCERROR_ARGUMENT_ERROR_VALUE_EXCEEDS_MAXIMUM,
		 "%s: shell item data size exceeds maximum.",
		 function );

		return( -1 );
	}
	/* Do not try to parse unsupported shell item data sizes
	 */
	if( shell_item_data_size < 12 )
	{
		return( 0 );
	}
	/* Do not try to parse unsupported shell item signatures
	 */
	if( memory_compare(
	     &( shell_item_data[ 6 ] ),
	     "CFSF",
	     4 ) != 0 )
	{
		return( 0 );
	}
	byte_stream_copy_to_uint32_little_endian(
	 &( shell_item_data[ 10 ] ),
	 data_size );

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "%s: class type indicator\t\t\t: 0x%02" PRIx8 "\n",
		 function,
		 shell_item_data[ 2 ] );

		libcnotify_printf(
		 "%s: unknown1\t\t\t\t: 0x%02" PRIx8 "\n",
		 function,
		 shell_item_data[ 3 ] );

		byte_stream_copy_to_uint16_little_endian(
		 &( shell_item_data[ 4 ] ),
		 value_16bit );
		libcnotify_printf(
		 "%s: unknown2\t\t\t\t: 0x%04" PRIx16 "\n",
		 function,
		 value_16bit );

		libcnotify_printf(
		 "%s: signature\t\t\t\t: %c%c%c%c\n",
		 function,
		 shell_item_data[ 6 ],
		 shell_item_data[ 7 ],
		 shell_item_data[ 8 ],
		 shell_item_data[ 9 ] );

		libcnotify_printf(
		 "%s: data size\t\t\t\t: %" PRIu16 "\n",
		 function,
		 data_size );
	}
#endif
	shell_item_data_offset = 12;

	if( data_size > 0 )
	{
		if( ( data_size < 2 )
		 && ( data_size > ( shell_item_data_size - 12 ) ) )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
			 "%s: invalid data size value out of bounds.",
			 function );

			return( -1 );
		}
		data_size -= 2;

#if defined( HAVE_DEBUG_OUTPUT )
		if( libcnotify_verbose != 0 )
		{
			libcnotify_printf(
			 "%s: data:\n",
			 function );
			libcnotify_print_data(
			 &( shell_item_data[ 12 ] ),
			 data_size,
			 LIBCNOTIFY_PRINT_DATA_FLAG_GROUP_DATA );
		}
#endif
	}
#if defined( HAVE_DEBUG_OUTPUT )
	else if( libcnotify_verbose != 0 )
	{
		libcnotify_printf(
		 "\n" );
	}
#endif
/* TODO move to sub item parsing ? */
	if( data_size >= 16 )
	{
#if defined( HAVE_DEBUG_OUTPUT )
		if( libcnotify_verbose != 0 )
		{
			byte_stream_copy_to_uint16_little_endian(
			 &( shell_item_data[ 12 ] ),
			 value_16bit );
			libcnotify_printf(
			 "%s: unknown3\t\t\t\t: 0x%04" PRIx16 "\n",
			 function,
			 value_16bit );

			byte_stream_copy_to_uint32_little_endian(
			 &( shell_item_data[ 14 ] ),
			 value_32bit );
			libcnotify_printf(
			 "%s: file size\t\t\t\t: %" PRIu32 "\n",
			 function,
			 value_32bit );

			if( libfwsi_debug_print_fat_date_time_value(
			     function,
			     "modification time\t\t\t",
			     &( shell_item_data[ 18 ] ),
			     4,
			     LIBFDATETIME_ENDIAN_LITTLE,
			     LIBFDATETIME_STRING_FORMAT_TYPE_CTIME | LIBFDATETIME_STRING_FORMAT_FLAG_DATE_TIME,
			     error ) != 1 )
			{
				libcerror_error_set(
				 error,
				 LIBCERROR_ERROR_DOMAIN_RUNTIME,
				 LIBCERROR_RUNTIME_ERROR_PRINT_FAILED,
				 "%s: unable to print FAT date time value.",
				 function );

				return( -1 );
			}
			byte_stream_copy_to_uint16_little_endian(
			 &( shell_item_data[ 22 ] ),
			 value_16bit );
			libcnotify_printf(
			 "%s: file attribute flags\t\t\t: 0x%04" PRIx16 "\n",
			 function,
			 value_16bit );
			libfwsi_file_attributes_print(
			 value_16bit );
			libcnotify_printf(
			 "\n" );
		}
#endif
		shell_item_data_offset += 12;

		for( string_size = shell_item_data_offset;
		     string_size < shell_item_data_size;
		     string_size++ )
		{
			if( shell_item_data[ string_size ] == 0 )
			{
				string_size++;

				break;
			}
		}
		string_size -= shell_item_data_offset;

		string_alignment_size = string_size % 2;

#if defined( HAVE_DEBUG_OUTPUT )
		if( libcnotify_verbose != 0 )
		{
			if( libfwsi_debug_print_string_value(
			     function,
			     "primary name\t\t\t\t",
			     &( shell_item_data[ shell_item_data_offset ] ),
			     string_size,
			     ascii_codepage,
			     error ) != 1 )
			{
				libcerror_error_set(
				 error,
				 LIBCERROR_ERROR_DOMAIN_RUNTIME,
				 LIBCERROR_RUNTIME_ERROR_PRINT_FAILED,
				 "%s: unable to print string value.",
				 function );

				return( -1 );
			}
		}
#endif
		shell_item_data_offset += string_size + string_alignment_size;

#if defined( HAVE_DEBUG_OUTPUT )
		if( libcnotify_verbose != 0 )
		{
			byte_stream_copy_to_uint16_little_endian(
			 &( shell_item_data[ shell_item_data_offset ] ),
			 value_16bit );

			libcnotify_printf(
			 "%s: unknown5\t\t\t\t: 0x%04" PRIx16 "\n",
			 function,
			 value_16bit );
		}
#endif
		shell_item_data_offset += 2;
	}
	if( shell_item_data_offset > ( shell_item_data_size - 32 ) )
	{
		libcerror_error_set(
		 error,
		 LIBCERROR_ERROR_DOMAIN_RUNTIME,
		 LIBCERROR_RUNTIME_ERROR_VALUE_OUT_OF_BOUNDS,
		 "%s: invalid shell item data size value out of bounds.",
		 function );

		return( -1 );
	}
#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		if( libfwsi_debug_print_guid_value(
		     function,
		     "delagate item class identifier\t",
		     &( shell_item_data[ shell_item_data_offset ] ),
		     16,
		     LIBFGUID_ENDIAN_LITTLE,
		     LIBFGUID_STRING_FORMAT_FLAG_USE_UPPER_CASE | LIBFGUID_STRING_FORMAT_FLAG_USE_SURROUNDING_BRACES,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_PRINT_FAILED,
			 "%s: unable to print GUID value.",
			 function );

			return( -1 );
		}
	}
#endif
	shell_item_data_offset += 16;

#if defined( HAVE_DEBUG_OUTPUT )
	if( libcnotify_verbose != 0 )
	{
		if( libfwsi_debug_print_guid_value(
		     function,
		     "item class identifier\t\t\t",
		     &( shell_item_data[ shell_item_data_offset ] ),
		     16,
		     LIBFGUID_ENDIAN_LITTLE,
		     LIBFGUID_STRING_FORMAT_FLAG_USE_UPPER_CASE | LIBFGUID_STRING_FORMAT_FLAG_USE_SURROUNDING_BRACES,
		     error ) != 1 )
		{
			libcerror_error_set(
			 error,
			 LIBCERROR_ERROR_DOMAIN_RUNTIME,
			 LIBCERROR_RUNTIME_ERROR_PRINT_FAILED,
			 "%s: unable to print GUID value.",
			 function );

			return( -1 );
		}
		libcnotify_printf(
		 "%s: shell folder name\t\t\t: %s\n",
		 function,
		 libfwsi_shell_folder_identifier_get_name(
		  &( shell_item_data[ shell_item_data_offset ] ) ) );

		libcnotify_printf(
		 "\n" );
	}
#endif
	shell_item_data_offset += 16;

	return( (ssize_t) shell_item_data_offset );
}

