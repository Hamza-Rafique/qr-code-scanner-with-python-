import cv2
from pyzbar import pyzbar

def decode_qr(frame):
    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        # Draw a rectangle around the QR code
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(points)
            points = hull.reshape(-1, 2)
        n = len(points)
        for j in range(0, n):
            cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (0, 255, 0), 3)

        # Extract QR code data
        qr_data = obj.data.decode("utf-8")
        qr_type = obj.type
        text = '{}: {}'.format(qr_type, qr_data)


        # Display the QR code data on the frame
        cv2.putText(frame, text, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Decode QR code from the current frame
    frame = decode_qr(frame)

    # Display the resulting frame
    cv2.imshow('QR Code Scanner', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
