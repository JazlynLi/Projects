; Some utility functions that you may find useful.
(define (apply-to-all proc items)
  (if (null? items)
      '()
      (cons (proc (car items))
            (apply-to-all proc (cdr items)))))

(define (keep-if predicate sequence)
  (cond ((null? sequence) nil)
        ((predicate (car sequence))
         (cons (car sequence)
               (keep-if predicate (cdr sequence))))
        (else (keep-if predicate (cdr sequence)))))

(define (accumulate op initial sequence)
  (if (null? sequence)
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))

; Problem 18
;; Turns a list of pairs into a pair of lists
(define (zip pairs)
  (cons (apply-to-all car pairs) (cons (apply-to-all cadr pairs) nil))
  )

(zip '())
; expect (() ())
(zip '((1 2)))
; expect ((1) (2))
(zip '((1 2) (3 4) (5 6)))
; expect ((1 3 5) (2 4 6))

; Problem 19

;; A list of all ways to partition TOTAL, where  each partition must
;; be at most MAX-VALUE and there are at most MAX-PIECES partitions.

; need to write comment, like what lst represents, detailed explanation

  (define (help-add value parts)
    (apply-to-all (lambda (part) (cons value part)) parts)
    )


(define (list-partitions total max-pieces max-value)
  ; (define (help-add value parts)
  ;   (apply-to-all (lambda (part) (cons value part)) parts)
  ;   )

  (cond
    ((< total 0) nil)
    ((= total 0) '(nil))
    ((= max-pieces 0) nil)
    ((= max-value 0) nil)
    (else
      (append (list-partitions total max-pieces (- max-value 1))
        (help-add max-value (list-partitions (- total max-value) (- max-pieces 1) max-value))
        )
      )
    )


  ; (define (partitions total piece value)
  ;   (cond
  ;     ((= total 0) '())
  ;     ((< total 0) nil)
  ;     ((= piece 0) nil)
  ;     ((= value 0) nil)

  ;   (else
  ;     (define no (partitions total piece (- value 1)))
  ;     (define yes (partitions (- total value) (- piece 1) value))
  ;     (define lst (apply-to-all (lambda (elem) (cons elem value)) yes))
  ;     (cons no yes))))
  ;     ;   (partitions (- total value) (- piece 1) value (cons value lst))

  ;     ; ))))
  ; (partitions total max-pieces max-value)

  ; )



    ; (define (all value lst)
    ;   (define (add-value elem)
    ;     (cons value elem)
    ;     )
    ;   (apply-to-all add-value lst)
    ;   )

    ; (cond
    ;   ((= total 0) '())
    ;   ((< total 0) nil)
    ;   ((= piece 0) nil)
    ;   ((= value 0) nil)
    ;   (else
    ;     (append (list-partitions total max-pieces (- max-value 1))
    ;       (all max-value (list-partitions (- total max-value) (- max-pieces 1) max-value)))
    ;   )




  ; (define (partitions total pieces value lst)
  ;   (cond
  ;     ((= total 0) '())
  ;     ((< total 0) nil)
  ;     ((= piece 0) nil)
  ;     ((= value 0) nil)
  ;     (else
  ;       (append (partitions total pieces (- value 1) lst)


  ;       )
  ;     )





  ; (define (helper value lst)
  ;   (define (add-value elem)
  ;     (cons value elem)
  ;     )
  ;   (apply-to-all add-value lst)
  ; )

  ; (cond
  ;     ((= total 0) '())
  ;     ((< total 0) nil)
  ;     ((= max-value 0) nil)
  ;     ((= max-pieces 0) nil)
  ;     (else  (append 
  ;               (list-partitions total max-pieces (- max-value 1))
  ;               (helper max-value (list-partitions (- total max-value) (- max-pieces 1) max-value)))
  ;            )
  ; )





  ; (define (partition total piece value lst)
  ;   (cond
  ;     ((= total 0) '())
  ;     ((< total 0) nil)
  ;     ((= value 0) nil)
  ;     ((= piece 0) nil)
  ;     (else 
  ;       (define lst (cons value (cons (partition (- total value) (- piece 1) value lst) nil)))
  ;       (append lst (partition total piece (- value 1) lst))
         
  ;         ; (define no (partition total piece (- value 1) lst))
  ;         ; (define yes (add-value value (partition (- total value) (- piece 1) value)))
  ;         ; (append no yes)

  ;         ; (partition total piece (- value 1) lst)
  ;         ; (partition (- total value) (- piece 1) value (append lst (list value))) )

  ;       )
  ;     )
  ; )

  ; (define (add-value value parts)
  ;   (append parts (list value)))

  ; (partition total max-pieces max-value '())
)

(list-partitions 5 2 4)
; expects a permutation of ((4 1) (3 2))
(list-partitions 7 3 5)
; expects a permutation of ((5 2) (5 1 1) (4 3) (4 2 1) (3 3 1) (3 2 2))


; Problem 20
;; Returns a function that takes in an expression and checks if it is the special
;; form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr)
         expr
         )
        ((quoted? expr)
          expr
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           (cons form (cons params (analyze body)))
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           (define lst (zip values))
           (display lst)
           (display '***)
           ; (cons (cons 'lambda (cons (cons (caar lst) nil) (analyze body))) 
           ;       (cadr lst))
              (cons (cons 'lambda (cons (car lst) (apply-to-all analyze body))) (apply-to-all analyze (cadr lst)))
           ))
        (else
         (cons (car expr)
          (apply-to-all analyze (cdr expr))
            )
         )
  ))

(analyze 1)
; expect 1
(analyze 'a)
; expect a
(analyze '(+ 1 2))
; expect (+ 1 2)

;; Quoted expressions remain the same
(analyze '(quote (let ((a 1) (b 2)) (+ a b))))
; expect (quote (let ((a 1) (b 2)) (+ a b)))

;; Lambda parameters not affected, but body affected
(analyze '(lambda (let a b) (+ let a b)))
; expect (lambda (let a b) (+ let a b))
(analyze '(lambda (x) a (let ((a x)) a)))
; expect (lambda (x) a ((lambda (a) a) x))

(analyze '(let ((a 1)
                (b 2))
            (+ a b)))
; expect ((lambda (a b) (+ a b)) 1 2)
(analyze '(let ((a (let ((a 2)) a))
                (b 2))
            (+ a b)))
; expect ((lambda (a b) (+ a b)) ((lambda (a) a) 2) 2)
(analyze '(let ((a 1))
            (let ((b a))
              b)))
; expect ((lambda (a) ((lambda (b) b) a)) 1)


;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
(define (hax d k)
  'YOUR-CODE-HERE
  nil)




