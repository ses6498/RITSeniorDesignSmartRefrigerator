#ifndef CANNONFIELD_H
#define CANNONFIELD_H

#include <QWidget>

class QTimer;

class CannonField : public QWidget
{
	Q_OBJECT

public:
	CannonField(QWidget *parent = 0);

	int angle() const {return currentAngle;}
	int force() const {return currentForce;}

public slots:
	void setAngle(int angle);
	void setForce (int force);
	void shoot();
	void newTarget();

private slots:
	void moveShot();

signals:
	void hit();
	void missed();
	void angleChanged(int newAngle);
	void forceChanged (int newForce);

protected: 
	void paintEvent(QPaintEvent *event);

private:
	void paintShot(QPainter &painter);
	void paintTarget (QPainter &painter);
	void paintCannon(QPainter &painter);
	QRect cannonRect() const;
	QRect shotRect() const;
	QRect targetRect() const;

	int currentAngle;
	int currentForce;

	int timerCount;
	QTimer *autoShootTimer;
	float shootAngle;
	float shootForce;

	QPoint target;
};

#endif
