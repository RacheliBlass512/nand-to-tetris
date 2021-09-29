// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(BIGLOOP)

    @SCREEN
    D=A
    @addr
    M=D  // addr = 16384

    @KBD
    D=M

    @BLACK
    D;JEQ

    (WHITE)
        @i
        M=0 //i=0
        (LOOP1)
            @i
            D=M
            @8192
            D=A-D
            @STOP1
            D;JEQ // if(8192-i==0)

            @addr
            A=M
            M=-1 // RAM[addr] = -1
            @i
            M=M+1  // i = i + 1
            @addr
            M=M+1  // addr = addr + 1
            @LOOP1
            0;JMP  // goto LOOP
        (STOP1)
            @BIGLOOP
            0;JMP

    (BLACK)
        @i
        M=0 //i=0
        (LOOP2)
            @i
            D=M
            @8192
            D=A-D
            @STOP2
            D;JEQ // if(8192-i==0)

            @addr
            A=M
            M=0 // RAM[addr] = 0
            @i
            M=M+1  // i = i + 1
            @addr
            M=M+1  // addr = addr + 1
            @LOOP2
            0;JMP  // goto LOOP
        (STOP2)
            @BIGLOOP
            0;JMP