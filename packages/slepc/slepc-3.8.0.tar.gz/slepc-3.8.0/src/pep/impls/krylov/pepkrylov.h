/*
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   SLEPc - Scalable Library for Eigenvalue Problem Computations
   Copyright (c) 2002-2017, Universitat Politecnica de Valencia, Spain

   This file is part of SLEPc.
   SLEPc is distributed under a 2-clause BSD license (see LICENSE).
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
*/
/*
   Private header for TOAR and STOAR
*/

#if !defined(__TOAR_H)
#define __TOAR_H

typedef struct {
  PetscReal   keep;         /* restart parameter */
  PetscBool   lock;         /* locking/non-locking variant */
  PetscReal   dtol;         /* tolerance for deflation */
  PetscInt    d;            /* polynomial degree */
  PetscInt    ld;           /* leading dimension of auxiliary matrices */
  PetscScalar *S,*qB;       /* auxiliary matrices */
} PEP_TOAR;

#endif

PETSC_INTERN PetscErrorCode PEPExtractVectors_TOAR(PEP);

