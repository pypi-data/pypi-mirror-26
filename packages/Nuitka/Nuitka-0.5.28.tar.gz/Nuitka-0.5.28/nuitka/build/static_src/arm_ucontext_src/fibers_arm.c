/* Extract of libtask, just the ARM specific portions. */

/*

This software was developed as part of a project at MIT.

Copyright (c) 2005-2007 Russ Cox,
                   Massachusetts Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

===

Contains parts of an earlier library that has:

 * The authors of this software are Rob Pike, Sape Mullender, and Russ Cox
 *       Copyright (c) 2003 by Lucent Technologies.
 * Permission to use, copy, modify, and distribute this software for any
 * purpose without fee is hereby granted, provided that this entire notice
 * is included in all copies of any software which is or includes a copy
 * or modification of this software and in all copies of the supporting
 * documentation for such software.
 * THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
 * WARRANTY.  IN PARTICULAR, NEITHER THE AUTHORS NOR LUCENT TECHNOLOGIES MAKE ANY
 * REPRESENTATION OR WARRANTY OF ANY KIND CONCERNING THE MERCHANTABILITY
 * OF THIS SOFTWARE OR ITS FITNESS FOR ANY PARTICULAR PURPOSE.
*/

// Implementation of process context switch for ARM

#include "nuitka/prelude.h"

#ifdef __cplusplus
extern "C" {
#endif

int getmcontext( mcontext_t *mcontext );
void setmcontext( const mcontext_t *mcontext );

#ifdef __cplusplus
}
#endif


#define setcontext(u) setmcontext( &(u)->uc_mcontext )
#define getcontext(u) getmcontext( &(u)->uc_mcontext )

void makecontext( ucontext_t *uc, void (*fn)(void), int argc, ... );

#define STACK_SIZE (1024*1024)

// Keep one stack around to avoid the overhead of repeated malloc/free in
// case of frequent instantiations in a loop.
static void *last_stack = NULL;

void _initFiber( Fiber *to )
{
    to->f_context.uc_stack.ss_sp = NULL;
    to->f_context.uc_link = NULL;
    to->start_stack = NULL;
}

int _prepareFiber( Fiber *to, void *code, uintptr_t arg )
{
    int res = getcontext( &to->f_context );
    if (unlikely( res != 0 ))
    {
        return 1;
    }

    to->f_context.uc_stack.ss_size = STACK_SIZE;
    to->f_context.uc_stack.ss_sp = last_stack ? last_stack : malloc( STACK_SIZE );
    to->start_stack = to->f_context.uc_stack.ss_sp;
    to->f_context.uc_link = NULL;
    last_stack = NULL;

    makecontext( &to->f_context, (void (*)())code, 1, (unsigned long)arg );

    return 0;
}

void _releaseFiber( Fiber *to )
{
    if ( to->start_stack != NULL )
    {
        if ( last_stack == NULL )
        {
            last_stack = to->start_stack;
        }
        else
        {
            free( to->start_stack );
        }

        to->start_stack = NULL;
    }
}

void _swapFiber( Fiber *to, Fiber *from )
{
    if ( getcontext( &to->f_context ) == 0 )
    {
        setcontext( &from->f_context );
    }
}
