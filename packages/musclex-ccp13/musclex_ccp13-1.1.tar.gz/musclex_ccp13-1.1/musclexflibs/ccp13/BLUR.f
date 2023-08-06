C     LAST UPDATE 06/10/98
C+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
C
      SUBROUTINE BLUR(BUF,CBACK,SMBUF,NPIX,NRAST,PWID,RWID,
     &                XC,YC,TEMPBUF,IFLAG,DOEDGE)
      IMPLICIT NONE
C
C Purpose: Blur background and subtract from pattern
C+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
C
C Arguements:
C
      INTEGER NPIX,NRAST,PWID,RWID
      REAL XC,YC
      REAL BUF(NPIX*NRAST),CBACK(NPIX*NRAST),SMBUF(PWID*RWID)
      REAL TEMPBUF(NPIX*NRAST) 
      INTEGER IFLAG(NPIX*NRAST)
      LOGICAL DOEDGE
C
C Local variables:
C
      INTEGER I,J,K,L,M,SPIX,SRAST,SPOINT
      INTEGER IFLAG2
C
C+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
C

C++++++++++  Blur background and put in TEMPBUF  +++++++++++++++++++++++

      DO 100 J=1,NRAST
        DO 90 I=1,NPIX

          M=(J-1)*NPIX+I
          IFLAG2=0
          TEMPBUF(M)=0.

          IF(IFLAG(M).EQ.1)THEN

            DO 80 L=1,RWID
              DO 70 K=1,PWID

                SPIX=(I+K-(PWID+1)/2)
                SRAST=(J+L-(RWID+1)/2)

                IF(SPIX.GT.0.AND.SPIX.LE.NPIX.AND.
     &             SRAST.GT.0.AND.SRAST.LE.NRAST)THEN

                   SPOINT=(SRAST-1)*NPIX+SPIX

                   IF(BUF(SPOINT).GT.-0.5E+30)THEN
                     TEMPBUF(M)=TEMPBUF(M)+CBACK(SPOINT)
     &                          *SMBUF((L-1)*PWID+K)
                   ELSE
                     IFLAG2=IFLAG2+1
                   ENDIF

                ELSE

                    IFLAG2=IFLAG2+1

                ENDIF

 70           CONTINUE
 80         CONTINUE

            IF(IFLAG2.GT.0)THEN
              TEMPBUF(M)=TEMPBUF(M)*( FLOAT(PWID*RWID)/
     &                   FLOAT(PWID*RWID-IFLAG2) )
            ENDIF


C+++  Subtract blurred background from pattern and put in TEMPBUF  +++

            TEMPBUF(M)=BUF(M)-TEMPBUF(M)

          ENDIF

 90     CONTINUE
 100  CONTINUE

      RETURN
      END
